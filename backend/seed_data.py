from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Initialize DB
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Clear existing data
    db.query(models.OutageEvent).delete()
    db.query(models.Customer).delete()
    db.query(models.FiberInfrastructure).delete()
    db.query(models.CLLILocation).delete()
    db.query(models.NetworkEquipment).delete()
    db.query(models.RepairCrew).delete()
    db.query(models.NOC).delete()
    db.query(models.NetworkEngineer).delete()
    db.query(models.Agent).delete()
    db.query(models.Supervisor).delete()
    db.query(models.ConstructionCompany).delete()
    db.query(models.IncidentTimeline).delete()
    db.query(models.CustomerInteraction).delete()
    db.query(models.SplicePoint).delete()

    # 1. NOC Operators
    nocs = [
        models.NOC(id="NOC-OPR-001", label="James Rodriguez", role="Senior Operator", level=3),
        models.NOC(id="NOC-OPR-002", label="Maria Thompson", role="Senior Operator", level=3),
        models.NOC(id="NOC-OPR-003", label="David Chen", role="Lead Operator", level=4),
    ]
    db.add_all(nocs)

    # 2. Network Engineers
    engineers = [
        models.NetworkEngineer(id="ENG-CA-001", label="Robert Martinez", specialization="GPON Specialist"),
        models.NetworkEngineer(id="ENG-CA-002", label="Jennifer Wong", specialization="GPON Specialist"),
        models.NetworkEngineer(id="ENG-CA-003", label="Michael Patel", specialization="Core Network"),
    ]
    db.add_all(engineers)

    # 3. Repair Crews
    crews = [
        models.RepairCrew(id="CREW-CA-NOR-012", label="Crew 012 (Thomas)", size=4, task="144-strand splice"),
        models.RepairCrew(id="CREW-CA-NOR-013", label="Crew 013 (Sarah)", size=3, task="96-strand splice"),
        models.RepairCrew(id="CREW-CA-NOR-014", label="Crew 014 (Marcus)", size=2, task="Conduit repair"),
    ]
    db.add_all(crews)

    # 4. Supervisors
    supervisors = [
        models.Supervisor(id="SUP-001", label="Michael Torres", role="Residential Support"),
        models.Supervisor(id="SUP-002", label="Robert Kim", role="Business Support"),
        models.Supervisor(id="SUP-003", label="IT Director", role="Internal IT"),
    ]
    db.add_all(supervisors)

    # 5. Agents
    agents = [
        models.Agent(id="AGT-001", label="James Rodriguez", role="Tech Support", supervisor_name="SUP-001"),
        models.Agent(id="AGT-002", label="Maria Thompson", role="Business Support", supervisor_name="SUP-002"),
    ]
    db.add_all(agents)

    # 6. CLLI Locations
    cllis = [
        models.CLLILocation(id="SNFCCA01", label="SF Central Office", status="AFFECTED", customers_affected=2847),
        models.CLLILocation(id="SNFCCA02", label="SF Secondary CO", status="AFFECTED", customers_affected=1709),
        models.CLLILocation(id="SNFCCA03", label="Backup Facility", status="OK", customers_affected=0),
    ]
    db.add_all(cllis)

    # 7. Fiber Infrastructure
    fibers = [
        models.FiberInfrastructure(id="FBR-CA-SNFC-TRUNK-A01", label="Main Trunk A01", status="DAMAGED", capacity="144 fibers", start_clli="SNFCCA01", end_clli="SNFCCA02"),
        models.FiberInfrastructure(id="FBR-CA-SNFC-TRUNK-A02", label="Secondary Trunk A02", status="DAMAGED", capacity="96 fibers", start_clli="SNFCCA01", end_clli="SNFCCA02"),
        models.FiberInfrastructure(id="FBR-CA-SNFC-TRUNK-B01", label="Backup Trunk B01", status="OK", capacity="288 fibers", start_clli="SNFCCA03", end_clli="SNFCCA04"),
        models.FiberInfrastructure(id="FBR-CA-INTERNAL-01", label="Corporate Network", status="DAMAGED", capacity="48 fibers", start_clli="SNFCCA01", end_clli="SNFCCA01"),
    ]
    db.add_all(fibers)

    # 8. Splice Points
    splices = [
        models.SplicePoint(id="SP-2847", label="Splice Point 2847", status="DESTROYED", fiber_cable_id="FBR-CA-SNFC-TRUNK-A01", repair_crew_id="CREW-CA-NOR-012"),
        models.SplicePoint(id="SP-1523", label="Splice Point 1523", status="DAMAGED", fiber_cable_id="FBR-CA-SNFC-TRUNK-A02", repair_crew_id="CREW-CA-NOR-013"),
        models.SplicePoint(id="CONDUIT-SNFC-01", label="Conduit SNFC-01", status="DESTROYED", fiber_cable_id="FBR-CA-INTERNAL-01", repair_crew_id="CREW-CA-NOR-014"),
    ]
    db.add_all(splices)

    # 9. Construction Companies
    construction = [
        models.ConstructionCompany(id="CONST-001", label="CalTrans Construction Inc", liability="Poor 811 compliance", cost="$284,500"),
    ]
    db.add_all(construction)

    # 10. Outage Events
    outages = [
        models.OutageEvent(id="OUT-2024-CA-001", type="Outage", label="Gigabit Fiber Res", customers_affected=2847, duration="8.5h", status="Resolved", noc_ticket_id="NOC-OPR-003", network_engineer_id="ENG-CA-001", repair_crew_id="CREW-CA-NOR-012", construction_company_id="CONST-001", fiber_cable_id="FBR-CA-SNFC-TRUNK-A01", clli="SNFCCA01"),
        models.OutageEvent(id="OUT-2024-CA-002", type="Outage", label="Business Fiber 500", customers_affected=412, duration="8.5h", status="Resolved", noc_ticket_id="NOC-OPR-003", network_engineer_id="ENG-CA-002", repair_crew_id="CREW-CA-NOR-012", construction_company_id="CONST-001", fiber_cable_id="FBR-CA-SNFC-TRUNK-A02", clli="SNFCCA02"),
        models.OutageEvent(id="OUT-2024-CA-003", type="Outage", label="Internal Network", customers_affected=23, duration="8.5h", status="Resolved", noc_ticket_id="NOC-OPR-001", network_engineer_id="ENG-CA-003", repair_crew_id="CREW-CA-NOR-014", construction_company_id="CONST-001", fiber_cable_id="FBR-CA-INTERNAL-01", clli="SNFCCA01"),
        models.OutageEvent(id="OUT-2024-CA-004", type="Outage", label="Gigabit Fiber Res Sec", customers_affected=1523, duration="5.25h", status="Resolved", noc_ticket_id="NOC-OPR-002", network_engineer_id="ENG-CA-001", repair_crew_id="CREW-CA-NOR-013", construction_company_id="CONST-001", fiber_cable_id="FBR-CA-SNFC-TRUNK-A01", clli="SNFCCA01"),
        models.OutageEvent(id="OUT-2024-CA-005", type="Outage", label="Business Fiber 1Gig Sec", customers_affected=186, duration="5.25h", status="Resolved", noc_ticket_id="NOC-OPR-002", network_engineer_id="ENG-CA-002", repair_crew_id="CREW-CA-NOR-013", construction_company_id="CONST-001", fiber_cable_id="FBR-CA-SNFC-TRUNK-A02", clli="SNFCCA02"),
    ]
    db.add_all(outages)

    # 11. Customers
    customers = [
        models.Customer(id="CUST-RES-001", label="Res. Customer 1", segment="Residential", connected_clli="SNFCCA01"),
        models.Customer(id="CUST-RES-002", label="Res. Customer 2", segment="Residential", connected_clli="SNFCCA01"),
        models.Customer(id="CUST-BUS-001", label="Tech Corp HQ", segment="Business", connected_clli="SNFCCA02"),
        models.Customer(id="CUST-INT-001", label="Internal IT", segment="Internal", connected_clli="SNFCCA01"),
    ]
    db.add_all(customers)

    # 12. Customer Interactions
    interactions = [
        models.CustomerInteraction(id="INT-001", label="Call #2849", channel="Phone", nps=4, customer_id="CUST-RES-001", outage_id="OUT-2024-CA-001", agent_name="James Rodriguez", agent_supervisor="Michael Torres", transcript_id="TR-001"),
        models.CustomerInteraction(id="INT-002", label="Chat #9921", channel="Chat", nps=6, customer_id="CUST-BUS-001", outage_id="OUT-2024-CA-002", agent_name="Maria Thompson", agent_supervisor="Robert Kim", transcript_id="TR-002"),
        models.CustomerInteraction(id="INT-003", label="SMS #8823", channel="SMS", nps=3, customer_id="CUST-RES-002", outage_id="OUT-2024-CA-001", agent_name="James Rodriguez", agent_supervisor="Michael Torres", transcript_id="TR-003"),
    ]
    db.add_all(interactions)

    # 13. Incident Timeline
    timeline = [
        models.IncidentTimeline(id="TL-001", label="Outage Start", time="06:15:00", description="Fiber severed", outage_event_id="OUT-2024-CA-001", actor_id="CONST-001"),
        models.IncidentTimeline(id="TL-002", label="NOC Response", time="06:17:32", description="NOC response initiated", outage_event_id="OUT-2024-CA-001", actor_id="NOC-OPR-003"),
        models.IncidentTimeline(id="TL-003", label="Crew Arrival", time="07:15:00", description="First crew arrives", outage_event_id="OUT-2024-CA-001", actor_id="CREW-CA-NOR-012"),
        models.IncidentTimeline(id="TL-004", label="Restoration 1", time="11:30:00", description="Secondary trunk restored", outage_event_id="OUT-2024-CA-004", actor_id="CREW-CA-NOR-013"),
        models.IncidentTimeline(id="TL-005", label="Restoration 2", time="14:45:00", description="Primary trunk restored", outage_event_id="OUT-2024-CA-001", actor_id="CREW-CA-NOR-012"),
    ]
    db.add_all(timeline)

    # 14. Network Equipment
    equipment = [
        models.NetworkEquipment(id="EQ-OLT-001", label="OLT-001", type="OLT", location_clli="SNFCCA01", connected_fiber_id="FBR-CA-SNFC-TRUNK-A01", outage_event_id="OUT-2024-CA-001"),
        models.NetworkEquipment(id="EQ-RTR-001", label="Core Router 001", type="Core Router", location_clli="SNFCCA01", connected_fiber_id="FBR-CA-INTERNAL-01", outage_event_id="OUT-2024-CA-003"),
    ]
    db.add_all(equipment)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully!")
