const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(cors());
app.use(express.json());

// Database Setup
const db = new sqlite3.Database('./gigapulse.db');

function initDB() {
    db.serialize(() => {
        // --- 1. OUTAGE_EVENTS ---
        db.run(`CREATE TABLE IF NOT EXISTS outage_events (
            id TEXT PRIMARY KEY, 
            type TEXT, 
            label TEXT, 
            customers_affected INTEGER, 
            duration TEXT, 
            status TEXT,
            noc_ticket_id TEXT,
            network_engineer_id TEXT,
            repair_crew_id TEXT,
            construction_company_id TEXT,
            fiber_cable_id TEXT,
            clli TEXT
        )`);

        // --- 2. CUSTOMER_INTERACTIONS ---
        db.run(`CREATE TABLE IF NOT EXISTS customer_interactions (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            channel TEXT, 
            nps INTEGER, 
            customer_id TEXT, 
            outage_id TEXT,
            agent_name TEXT,
            agent_supervisor TEXT,
            transcript_id TEXT
        )`);

        // --- 3. NOC_OPERATORS ---
        db.run(`CREATE TABLE IF NOT EXISTS noc_operators (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            role TEXT,
            level INTEGER,
            noc_ticket_id TEXT
        )`);

        // --- 4. NETWORK_ENGINEERS ---
        db.run(`CREATE TABLE IF NOT EXISTS network_engineers (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            specialization TEXT,
            noc_ticket_id TEXT,
            fiber_cable_id TEXT
        )`);

        // --- 5. REPAIR_CREWS ---
        db.run(`CREATE TABLE IF NOT EXISTS repair_crews (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            size INTEGER, 
            task TEXT,
            noc_ticket_id TEXT,
            fiber_cable_id TEXT,
            splice_point_id TEXT
        )`);

        // --- 6. AGENTS ---
        db.run(`CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            role TEXT,
            supervisor_name TEXT
        )`);

        // --- 7. SUPERVISORS ---
        db.run(`CREATE TABLE IF NOT EXISTS supervisors (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            role TEXT
        )`);

        // --- 8. FIBER_INFRASTRUCTURE ---
        db.run(`CREATE TABLE IF NOT EXISTS fiber_infrastructure (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            status TEXT, 
            capacity TEXT,
            start_clli TEXT,
            end_clli TEXT
        )`);

        // --- 9. CONSTRUCTION_COMPANIES ---
        db.run(`CREATE TABLE IF NOT EXISTS construction_companies (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            liability TEXT, 
            cost TEXT,
            noc_ticket_id TEXT
        )`);

        // --- 10. CUSTOMERS ---
        db.run(`CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            segment TEXT,
            connected_clli TEXT
        )`);

        // --- 11. SPLICE_POINTS ---
        db.run(`CREATE TABLE IF NOT EXISTS splice_points (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            status TEXT,
            fiber_cable_id TEXT,
            repair_crew_id TEXT
        )`);

        // --- 12. CLLI_LOCATIONS ---
        db.run(`CREATE TABLE IF NOT EXISTS clli_locations (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            status TEXT,
            customers_affected INTEGER
        )`);

        // --- 13. INCIDENT_TIMELINE ---
        db.run(`CREATE TABLE IF NOT EXISTS incident_timeline (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            time TEXT,
            description TEXT,
            outage_event_id TEXT,
            actor_id TEXT
        )`);

        // --- 14. NETWORK_EQUIPMENT ---
        db.run(`CREATE TABLE IF NOT EXISTS network_equipment (
            id TEXT PRIMARY KEY, 
            label TEXT, 
            type TEXT,
            location_clli TEXT,
            connected_fiber_id TEXT,
            outage_event_id TEXT
        )`);

        // ================= SEED DATA =================

        // 1. Outage Events
        const stmtOutage = db.prepare("INSERT OR REPLACE INTO outage_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
        stmtOutage.run("OUT-2024-CA-001", "Outage", "Gigabit Fiber Res", 2847, "8.5h", "Resolved", "NOC-OPR-003", "ENG-CA-001", "CREW-CA-NOR-012", "CONST-001", "FBR-CA-SNFC-TRUNK-A01", "SNFCCA01");
        stmtOutage.run("OUT-2024-CA-002", "Outage", "Business Fiber 500", 412, "8.5h", "Resolved", "NOC-OPR-003", "ENG-CA-002", "CREW-CA-NOR-012", "CONST-001", "FBR-CA-SNFC-TRUNK-A02", "SNFCCA02");
        stmtOutage.run("OUT-2024-CA-003", "Outage", "Internal Network", 23, "8.5h", "Resolved", "NOC-OPR-001", "ENG-CA-003", "CREW-CA-NOR-014", "CONST-001", "FBR-CA-INTERNAL-01", "SNFCCA01");
        stmtOutage.run("OUT-2024-CA-004", "Outage", "Gigabit Fiber Res Sec", 1523, "5.25h", "Resolved", "NOC-OPR-002", "ENG-CA-001", "CREW-CA-NOR-013", "CONST-001", "FBR-CA-SNFC-TRUNK-A01", "SNFCCA01");
        stmtOutage.run("OUT-2024-CA-005", "Outage", "Business Fiber 1Gig Sec", 186, "5.25h", "Resolved", "NOC-OPR-002", "ENG-CA-002", "CREW-CA-NOR-013", "CONST-001", "FBR-CA-SNFC-TRUNK-A02", "SNFCCA02");
        stmtOutage.finalize();

        // 2. Customer Interactions
        const stmtInter = db.prepare("INSERT OR REPLACE INTO customer_interactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
        stmtInter.run("INT-001", "Call #2849", "Phone", 4, "CUST-RES-001", "OUT-2024-CA-001", "James Rodriguez", "Michael Torres", "TR-001");
        stmtInter.run("INT-002", "Chat #9921", "Chat", 6, "CUST-BUS-001", "OUT-2024-CA-002", "Maria Thompson", "Robert Kim", "TR-002");
        stmtInter.run("INT-003", "SMS #8823", "SMS", 3, "CUST-RES-002", "OUT-2024-CA-001", "James Rodriguez", "Michael Torres", "TR-003");
        stmtInter.finalize();

        // 3. NOC Operators
        const stmtNoc = db.prepare("INSERT OR REPLACE INTO noc_operators VALUES (?, ?, ?, ?, ?)");
        stmtNoc.run("NOC-OPR-001", "James Rodriguez", "Senior Operator", 3, "OUT-2024-CA-003");
        stmtNoc.run("NOC-OPR-002", "Maria Thompson", "Senior Operator", 3, "OUT-2024-CA-004");
        stmtNoc.run("NOC-OPR-003", "David Chen", "Lead Operator", 4, "OUT-2024-CA-001");
        stmtNoc.finalize();

        // 4. Network Engineers
        const stmtEng = db.prepare("INSERT OR REPLACE INTO network_engineers VALUES (?, ?, ?, ?, ?)");
        stmtEng.run("ENG-CA-001", "Robert Martinez", "GPON Specialist", "OUT-2024-CA-001", "FBR-CA-SNFC-TRUNK-A01");
        stmtEng.run("ENG-CA-002", "Jennifer Wong", "GPON Specialist", "OUT-2024-CA-002", "FBR-CA-SNFC-TRUNK-A02");
        stmtEng.run("ENG-CA-003", "Michael Patel", "Core Network", "OUT-2024-CA-003", "FBR-CA-INTERNAL-01");
        stmtEng.finalize();

        // 5. Repair Crews
        const stmtCrew = db.prepare("INSERT OR REPLACE INTO repair_crews VALUES (?, ?, ?, ?, ?, ?, ?)");
        stmtCrew.run("CREW-CA-NOR-012", "Crew 012 (Thomas)", 4, "144-strand splice", "OUT-2024-CA-001", "FBR-CA-SNFC-TRUNK-A01", "SP-2847");
        stmtCrew.run("CREW-CA-NOR-013", "Crew 013 (Sarah)", 3, "96-strand splice", "OUT-2024-CA-004", "FBR-CA-SNFC-TRUNK-A02", "SP-1523");
        stmtCrew.run("CREW-CA-NOR-014", "Crew 014 (Marcus)", 2, "Conduit repair", "OUT-2024-CA-003", "FBR-CA-INTERNAL-01", "CONDUIT-SNFC-01");
        stmtCrew.finalize();

        // 6. Agents
        const stmtAgent = db.prepare("INSERT OR REPLACE INTO agents VALUES (?, ?, ?, ?)");
        stmtAgent.run("AGT-001", "James Rodriguez", "Tech Support", "Michael Torres");
        stmtAgent.run("AGT-002", "Maria Thompson", "Business Support", "Robert Kim");
        stmtAgent.finalize();

        // 7. Supervisors
        const stmtSup = db.prepare("INSERT OR REPLACE INTO supervisors VALUES (?, ?, ?)");
        stmtSup.run("SUP-001", "Michael Torres", "Residential Support");
        stmtSup.run("SUP-002", "Robert Kim", "Business Support");
        stmtSup.run("SUP-003", "IT Director", "Internal IT");
        stmtSup.finalize();

        // 8. Fiber Infrastructure
        const stmtFiber = db.prepare("INSERT OR REPLACE INTO fiber_infrastructure VALUES (?, ?, ?, ?, ?, ?)");
        stmtFiber.run("FBR-CA-SNFC-TRUNK-A01", "Main Trunk A01", "DAMAGED", "144 fibers", "SNFCCA01", "SNFCCA02");
        stmtFiber.run("FBR-CA-SNFC-TRUNK-A02", "Secondary Trunk A02", "DAMAGED", "96 fibers", "SNFCCA01", "SNFCCA02");
        stmtFiber.run("FBR-CA-SNFC-TRUNK-B01", "Backup Trunk B01", "OK", "288 fibers", "SNFCCA03", "SNFCCA04");
        stmtFiber.run("FBR-CA-INTERNAL-01", "Corporate Network", "DAMAGED", "48 fibers", "SNFCCA01", "SNFCCA01");
        stmtFiber.finalize();

        // 9. Construction Companies
        const stmtConst = db.prepare("INSERT OR REPLACE INTO construction_companies VALUES (?, ?, ?, ?, ?)");
        stmtConst.run("CONST-001", "CalTrans Construction Inc", "Poor 811 compliance", "$284,500", "OUT-2024-CA-001");
        stmtConst.finalize();

        // 10. Customers
        const stmtCust = db.prepare("INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?)");
        stmtCust.run("CUST-RES-001", "Res. Customer 1", "Residential", "SNFCCA01");
        stmtCust.run("CUST-RES-002", "Res. Customer 2", "Residential", "SNFCCA01");
        stmtCust.run("CUST-BUS-001", "Tech Corp HQ", "Business", "SNFCCA02");
        stmtCust.run("CUST-INT-001", "Internal IT", "Internal", "SNFCCA01");
        stmtCust.finalize();

        // 11. Splice Points
        const stmtSplice = db.prepare("INSERT OR REPLACE INTO splice_points VALUES (?, ?, ?, ?, ?)");
        stmtSplice.run("SP-2847", "Splice Point 2847", "DESTROYED", "FBR-CA-SNFC-TRUNK-A01", "CREW-CA-NOR-012");
        stmtSplice.run("SP-1523", "Splice Point 1523", "DAMAGED", "FBR-CA-SNFC-TRUNK-A02", "CREW-CA-NOR-013");
        stmtSplice.run("CONDUIT-SNFC-01", "Conduit SNFC-01", "DESTROYED", "FBR-CA-INTERNAL-01", "CREW-CA-NOR-014");
        stmtSplice.finalize();

        // 12. CLLI Locations
        const stmtClli = db.prepare("INSERT OR REPLACE INTO clli_locations VALUES (?, ?, ?, ?)");
        stmtClli.run("SNFCCA01", "SF Central Office", "AFFECTED", 2847);
        stmtClli.run("SNFCCA02", "SF Secondary CO", "AFFECTED", 1709);
        stmtClli.run("SNFCCA03", "Backup Facility", "OK", 0);
        stmtClli.finalize();

        // 13. Incident Timeline
        const stmtTime = db.prepare("INSERT OR REPLACE INTO incident_timeline VALUES (?, ?, ?, ?, ?, ?)");
        stmtTime.run("TL-001", "Outage Start", "06:15:00", "Fiber severed", "OUT-2024-CA-001", "CONST-001");
        stmtTime.run("TL-002", "NOC Response", "06:17:32", "NOC response initiated", "OUT-2024-CA-001", "NOC-OPR-003");
        stmtTime.run("TL-003", "Crew Arrival", "07:15:00", "First crew arrives", "OUT-2024-CA-001", "CREW-CA-NOR-012");
        stmtTime.run("TL-004", "Restoration 1", "11:30:00", "Secondary trunk restored", "OUT-2024-CA-004", "CREW-CA-NOR-013");
        stmtTime.run("TL-005", "Restoration 2", "14:45:00", "Primary trunk restored", "OUT-2024-CA-001", "CREW-CA-NOR-012");
        stmtTime.finalize();

        // 14. Network Equipment
        const stmtEquip = db.prepare("INSERT OR REPLACE INTO network_equipment VALUES (?, ?, ?, ?, ?, ?)");
        stmtEquip.run("EQ-OLT-001", "OLT-001", "OLT", "SNFCCA01", "FBR-CA-SNFC-TRUNK-A01", "OUT-2024-CA-001");
        stmtEquip.run("EQ-RTR-001", "Core Router 001", "Core Router", "SNFCCA01", "FBR-CA-INTERNAL-01", "OUT-2024-CA-003");
        stmtEquip.finalize();
    });
}

initDB();

// API Endpoints

// Graph Data Endpoint
app.get('/api/graph/data', (req, res) => {
    const nodes = [];
    const links = [];

    db.serialize(() => {
        const queries = [
            { table: 'outage_events', group: 'outage', val: 25 },
            { table: 'customers', group: 'customer', val: 5 },
            { table: 'fiber_infrastructure', group: 'infra', val: 15 },
            { table: 'clli_locations', group: 'facility', val: 18 },
            { table: 'repair_crews', group: 'crew', val: 10 },
            { table: 'noc_operators', group: 'noc', val: 10 },
            { table: 'network_engineers', group: 'noc', val: 10 }, // Grouping engineers with NOC for color
            { table: 'agents', group: 'agent', val: 8 },
            { table: 'supervisors', group: 'agent', val: 12 }, // Grouping supervisors with agents
            { table: 'construction_companies', group: 'construction', val: 20 },
            { table: 'splice_points', group: 'infra', val: 8 },
            { table: 'network_equipment', group: 'equipment', val: 12 },
            { table: 'incident_timeline', group: 'interaction', val: 3 }, // Using interaction color for timeline
            { table: 'customer_interactions', group: 'interaction', val: 4 }
        ];

        let completed = 0;

        queries.forEach(q => {
            db.all(`SELECT * FROM ${q.table}`, (err, rows) => {
                if (err) console.error(err);
                else {
                    rows.forEach(r => nodes.push({ ...r, group: q.group, val: q.val }));
                }
                completed++;
                if (completed === queries.length) {
                    buildLinks(nodes, links, res);
                }
            });
        });
    });
});

function buildLinks(nodes, links, res) {
    // Helper to find node by ID
    const findNode = (id) => nodes.find(n => n.id === id);

    nodes.forEach(node => {
        // 1. Outage Events Links
        if (node.group === 'outage') {
            if (node.noc_ticket_id) links.push({ source: node.id, target: node.noc_ticket_id, name: 'Managed By' });
            if (node.network_engineer_id) links.push({ source: node.id, target: node.network_engineer_id, name: 'Assigned To' });
            if (node.repair_crew_id) links.push({ source: node.id, target: node.repair_crew_id, name: 'Assigned To' });
            if (node.construction_company_id) links.push({ source: node.id, target: node.construction_company_id, name: 'Caused By' });
            if (node.fiber_cable_id) links.push({ source: node.id, target: node.fiber_cable_id, name: 'Damaged' });
            if (node.clli) links.push({ source: node.id, target: node.clli, name: 'Location' });
        }

        // 2. Customer Interactions Links
        if (node.group === 'interaction' && node.customer_id) {
            links.push({ source: node.id, target: node.customer_id, name: 'By Customer' });
            if (node.outage_id) links.push({ source: node.id, target: node.outage_id, name: 'About Outage' });
            // Link to agent by name matching (simplified)
            if (node.agent_name) {
                const agent = nodes.find(n => n.label === node.agent_name && n.group === 'agent');
                if (agent) links.push({ source: node.id, target: agent.id, name: 'Handled By' });
            }
        }

        // 3. Agents Links
        if (node.group === 'agent' && node.supervisor_name) {
            const sup = nodes.find(n => n.label === node.supervisor_name && n.group === 'agent'); // Supervisors are in agent group
            if (sup) links.push({ source: node.id, target: sup.id, name: 'Reports To' });
        }

        // 4. Fiber Infrastructure Links
        if (node.group === 'infra' && node.start_clli) {
            links.push({ source: node.id, target: node.start_clli, name: 'Starts At' });
            if (node.end_clli) links.push({ source: node.id, target: node.end_clli, name: 'Ends At' });
        }

        // 5. Splice Points Links
        if (node.group === 'infra' && node.fiber_cable_id) { // Splice points are in infra group
            links.push({ source: node.id, target: node.fiber_cable_id, name: 'On Cable' });
            if (node.repair_crew_id) links.push({ source: node.id, target: node.repair_crew_id, name: 'Repaired By' });
        }

        // 6. Customers Links
        if (node.group === 'customer' && node.connected_clli) {
            links.push({ source: node.id, target: node.connected_clli, name: 'Connected To' });
        }

        // 7. Network Equipment Links
        if (node.group === 'equipment') {
            if (node.location_clli) links.push({ source: node.id, target: node.location_clli, name: 'Located At' });
            if (node.connected_fiber_id) links.push({ source: node.id, target: node.connected_fiber_id, name: 'Connects' });
            if (node.outage_event_id) links.push({ source: node.id, target: node.outage_event_id, name: 'Affected By' });
        }

        // 8. Timeline Links
        if (node.group === 'interaction' && node.time) { // Timeline events
            if (node.outage_event_id) links.push({ source: node.id, target: node.outage_event_id, name: 'Timeline' });
            if (node.actor_id) links.push({ source: node.id, target: node.actor_id, name: 'Involved' });
        }
    });

    res.json({ nodes, links });
}

// AI Agents
app.get('/api/agents/topology', (req, res) => {
    db.all("SELECT * FROM fiber_infrastructure WHERE status = 'DAMAGED'", (err, rows) => {
        const results = rows.map(row => ({
            id: row.id,
            issue: "Critical Link Failure",
            impact: "High - No Redundancy Detected",
            recommendation: "Reroute traffic via Backup Trunk B01"
        }));
        res.json(results);
    });
});

// WebSocket
wss.on('connection', (ws) => {
    console.log('Client connected');
    ws.send(JSON.stringify({ type: 'info', message: 'Connected to GigaPulse Live Stream' }));
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`GigaPulse Node.js Server running on port ${PORT}`);
});
