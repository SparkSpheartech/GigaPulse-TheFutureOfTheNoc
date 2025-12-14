from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/data")
def get_graph_data(db: Session = Depends(get_db)):
    # Fetch all entities
    outages = db.query(models.OutageEvent).all()
    customers = db.query(models.Customer).all()
    infra = db.query(models.FiberInfrastructure).all()
    cllis = db.query(models.CLLILocation).all()
    equipment = db.query(models.NetworkEquipment).all()
    crews = db.query(models.RepairCrew).all()
    noc = db.query(models.NOC).all()
    engineers = db.query(models.NetworkEngineer).all()
    agents = db.query(models.Agent).all()
    supervisors = db.query(models.Supervisor).all()
    construction = db.query(models.ConstructionCompany).all()
    timeline = db.query(models.IncidentTimeline).all()
    interactions = db.query(models.CustomerInteraction).all()
    splices = db.query(models.SplicePoint).all()

    nodes = []
    links = []

    # Helper to add node
    def add_node(entity, group, val=10):
        nodes.append({
            "id": entity.id,
            "label": entity.label,
            "group": group,
            "val": val,
            **{k: v for k, v in entity.__dict__.items() if not k.startswith('_')}
        })

    # Build Nodes
    for o in outages: add_node(o, "outage", 25)
    for c in customers: add_node(c, "customer", 5)
    for i in infra: add_node(i, "infra", 15)
    for l in cllis: add_node(l, "facility", 18)
    for e in equipment: add_node(e, "equipment", 12)
    for cr in crews: add_node(cr, "crew", 10)
    for n in noc: add_node(n, "noc", 10)
    for eng in engineers: add_node(eng, "noc", 10) # Group engineers with NOC
    for a in agents: add_node(a, "agent", 8)
    for s in supervisors: add_node(s, "agent", 12) # Group supervisors with agents
    for co in construction: add_node(co, "construction", 20)
    for t in timeline: add_node(t, "interaction", 5) # Use interaction color for timeline
    for intx in interactions: add_node(intx, "interaction", 4)
    for sp in splices: add_node(sp, "infra", 8)

    # Build Links
    
    # Outage Events
    for o in outages:
        if o.noc_ticket_id: links.append({"source": o.id, "target": o.noc_ticket_id, "name": "Managed By"})
        if o.network_engineer_id: links.append({"source": o.id, "target": o.network_engineer_id, "name": "Assigned To"})
        if o.repair_crew_id: links.append({"source": o.id, "target": o.repair_crew_id, "name": "Assigned To"})
        if o.construction_company_id: links.append({"source": o.id, "target": o.construction_company_id, "name": "Caused By"})
        if o.fiber_cable_id: links.append({"source": o.id, "target": o.fiber_cable_id, "name": "Damaged"})
        if o.clli: links.append({"source": o.id, "target": o.clli, "name": "Location"})

    # Customer Interactions
    for intx in interactions:
        if intx.customer_id: links.append({"source": intx.id, "target": intx.customer_id, "name": "By Customer"})
        if intx.outage_id: links.append({"source": intx.id, "target": intx.outage_id, "name": "About Outage"})
        # Agent link by name matching
        if intx.agent_name:
            agent = next((a for a in agents if a.label == intx.agent_name), None)
            if agent: links.append({"source": intx.id, "target": agent.id, "name": "Handled By"})

    # Agents
    for a in agents:
        if a.supervisor_name: links.append({"source": a.id, "target": a.supervisor_name, "name": "Reports To"})

    # Fiber Infrastructure
    for i in infra:
        if i.start_clli: links.append({"source": i.id, "target": i.start_clli, "name": "Starts At"})
        if i.end_clli: links.append({"source": i.id, "target": i.end_clli, "name": "Ends At"})

    # Splice Points
    for sp in splices:
        if sp.fiber_cable_id: links.append({"source": sp.id, "target": sp.fiber_cable_id, "name": "On Cable"})
        if sp.repair_crew_id: links.append({"source": sp.id, "target": sp.repair_crew_id, "name": "Repaired By"})

    # Customers
    for c in customers:
        if c.connected_clli: links.append({"source": c.id, "target": c.connected_clli, "name": "Connected To"})

    # Network Equipment
    for e in equipment:
        if e.location_clli: links.append({"source": e.id, "target": e.location_clli, "name": "Located At"})
        if e.connected_fiber_id: links.append({"source": e.id, "target": e.connected_fiber_id, "name": "Connects"})
        if e.outage_event_id: links.append({"source": e.id, "target": e.outage_event_id, "name": "Affected By"})

    # Timeline
    for t in timeline:
        if t.outage_event_id: links.append({"source": t.id, "target": t.outage_event_id, "name": "Timeline"})
        if t.actor_id: links.append({"source": t.id, "target": t.actor_id, "name": "Involved"})

    return {"nodes": nodes, "links": links}
