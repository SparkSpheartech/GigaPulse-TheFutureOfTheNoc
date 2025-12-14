from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base

class OutageEvent(Base):
    __tablename__ = "outage_events"
    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    label = Column(String)
    customers_affected = Column(Integer)
    duration = Column(String)
    status = Column(String)
    
    noc_ticket_id = Column(String, ForeignKey("noc_operators.id"))
    network_engineer_id = Column(String, ForeignKey("network_engineers.id"))
    repair_crew_id = Column(String, ForeignKey("repair_crews.id"))
    construction_company_id = Column(String, ForeignKey("construction_companies.id"))
    fiber_cable_id = Column(String, ForeignKey("fiber_infrastructure.id"))
    clli = Column(String, ForeignKey("clli_locations.id"))

    # Relationships
    interactions = relationship("CustomerInteraction", back_populates="outage")
    noc_operator = relationship("NOC", back_populates="outages")
    network_engineer = relationship("NetworkEngineer", back_populates="outages")
    repair_crew = relationship("RepairCrew", back_populates="outages")
    construction_company = relationship("ConstructionCompany", back_populates="outages")
    fiber_cable = relationship("FiberInfrastructure", back_populates="outages")
    clli_location = relationship("CLLILocation", back_populates="outages")
    timeline_events = relationship("IncidentTimeline", back_populates="outage")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    segment = Column(String)
    connected_clli = Column(String, ForeignKey("clli_locations.id"))
    
    interactions = relationship("CustomerInteraction", back_populates="customer")
    clli_location = relationship("CLLILocation", back_populates="customers")

class CustomerInteraction(Base):
    __tablename__ = "customer_interactions"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    channel = Column(String)
    nps = Column(Integer)
    
    customer_id = Column(String, ForeignKey("customers.id"))
    outage_id = Column(String, ForeignKey("outage_events.id"))
    agent_name = Column(String) # Simplified for now, could be FK to Agent
    agent_supervisor = Column(String)
    transcript_id = Column(String)
    
    customer = relationship("Customer", back_populates="interactions")
    outage = relationship("OutageEvent", back_populates="interactions")

class NOC(Base):
    __tablename__ = "noc_operators"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    role = Column(String)
    level = Column(Integer)
    
    outages = relationship("OutageEvent", back_populates="noc_operator")

class NetworkEngineer(Base):
    __tablename__ = "network_engineers"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    specialization = Column(String)
    
    outages = relationship("OutageEvent", back_populates="network_engineer")

class RepairCrew(Base):
    __tablename__ = "repair_crews"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    size = Column(Integer)
    task = Column(String)
    
    outages = relationship("OutageEvent", back_populates="repair_crew")
    splice_points = relationship("SplicePoint", back_populates="repair_crew")

class Agent(Base):
    __tablename__ = "agents"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    role = Column(String)
    supervisor_name = Column(String, ForeignKey("supervisors.id"))
    
    supervisor = relationship("Supervisor", back_populates="agents")

class Supervisor(Base):
    __tablename__ = "supervisors"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    role = Column(String)
    
    agents = relationship("Agent", back_populates="supervisor")

class FiberInfrastructure(Base):
    __tablename__ = "fiber_infrastructure"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    status = Column(String)
    capacity = Column(String)
    start_clli = Column(String, ForeignKey("clli_locations.id"))
    end_clli = Column(String, ForeignKey("clli_locations.id")) # Self-referential or to same table
    
    outages = relationship("OutageEvent", back_populates="fiber_cable")
    splice_points = relationship("SplicePoint", back_populates="fiber_cable")
    # For simplicity, not modeling start/end clli relationships explicitly to avoid circular dependency issues in this simple setup, 
    # but they are FKs.

class ConstructionCompany(Base):
    __tablename__ = "construction_companies"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    liability = Column(String)
    cost = Column(String)
    
    outages = relationship("OutageEvent", back_populates="construction_company")

class SplicePoint(Base):
    __tablename__ = "splice_points"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    status = Column(String)
    fiber_cable_id = Column(String, ForeignKey("fiber_infrastructure.id"))
    repair_crew_id = Column(String, ForeignKey("repair_crews.id"))
    
    fiber_cable = relationship("FiberInfrastructure", back_populates="splice_points")
    repair_crew = relationship("RepairCrew", back_populates="splice_points")

class CLLILocation(Base):
    __tablename__ = "clli_locations"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    status = Column(String)
    customers_affected = Column(Integer)
    
    outages = relationship("OutageEvent", back_populates="clli_location")
    customers = relationship("Customer", back_populates="clli_location")
    network_equipment = relationship("NetworkEquipment", back_populates="clli_location")

class IncidentTimeline(Base):
    __tablename__ = "incident_timeline"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    time = Column(String)
    description = Column(String)
    outage_event_id = Column(String, ForeignKey("outage_events.id"))
    actor_id = Column(String) # Generic link to actor
    
    outage = relationship("OutageEvent", back_populates="timeline_events")

class NetworkEquipment(Base):
    __tablename__ = "network_equipment"
    id = Column(String, primary_key=True, index=True)
    label = Column(String)
    type = Column(String)
    location_clli = Column(String, ForeignKey("clli_locations.id"))
    connected_fiber_id = Column(String) # Simplified
    outage_event_id = Column(String) # Simplified
    
    clli_location = relationship("CLLILocation", back_populates="network_equipment")
