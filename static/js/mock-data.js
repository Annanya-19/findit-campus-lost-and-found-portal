/**
 * FindIt - Mock Data for Frontend Preview & Local Testing
 * Covers all 8 categories and exact database fields:
 * item_name, item_description, category, item_type, location, date_lost_found, image, reported_by
 */

const MOCK_ITEMS = [
  {
    id: 1,
    item_name: "AirPods Pro (2nd Gen)",
    item_description: "White charging case with a small Pikachu sticker on the back. Left pod is slightly scratched. Left inside a transparent silicone protective sleeve.",
    category: "Electronics",
    item_type: "Lost",
    location: "Central Library, 2nd Floor Study Table 14",
    date_lost_found: "2026-11-20",
    image: "static/images/placeholder.svg",
    status: "Active",
    reported_by: {
      name: "Rohan Kulkarni",
      role: "Student",
      department: "Computer Engineering (3rd Year)",
      verified: true
    }
  },
  {
    id: 2,
    item_name: "Student ID Card & Metro Pass",
    item_description: "College ID Card belonging to CS Department along with a blue metro smart card inside a transparent holder with college lanyard.",
    category: "Documents / ID Cards",
    item_type: "Found",
    location: "Cafeteria Counter 3",
    date_lost_found: "2026-11-21",
    image: "static/images/placeholder.svg",
    status: "Active",
    reported_by: {
      name: "Sunita Rao",
      role: "Campus Staff",
      department: "Cafeteria Administration",
      verified: true
    }
  },
  {
    id: 3,
    item_name: "Black Wildcraft Laptop Backpack",
    item_description: "Contains engineering notebooks, a blue pencil pouch, and a steel water bottle in the side pocket. Left near auditorium reception seating area.",
    category: "Bags",
    item_type: "Lost",
    location: "Auditorium Main Lobby",
    date_lost_found: "2026-11-19",
    image: "static/images/placeholder.svg",
    status: "Active",
    reported_by: {
      name: "Amit Patel",
      role: "Student",
      department: "Mechanical Engineering (2nd Year)",
      verified: true
    }
  },
  {
    id: 4,
    item_name: "Navy Blue College Fest Hoodie (Size L)",
    item_description: "Annual Fest 2025 commemorative hoodie with embroidered college crest on chest and student coordinator badge on left sleeve.",
    category: "Clothing",
    item_type: "Found",
    location: "Sports Ground Bleachers",
    date_lost_found: "2026-11-21",
    image: "static/images/placeholder.svg",
    status: "Active",
    reported_by: {
      name: "Vikram Malhotra",
      role: "Faculty Coordinator",
      department: "Physical Education Dept.",
      verified: true
    }
  },
  {
    id: 5,
    item_name: "Higher Engineering Mathematics - B.S. Grewal",
    item_description: "Hardcover textbook with handwritten notes and yellow highlighter markings in Unit 3 (Differential Equations). Name written on inside page.",
    category: "Books / Stationery",
    item_type: "Lost",
    location: "Room 304, Academic Block B",
    date_lost_found: "2026-11-18",
    image: "static/images/placeholder.svg",
    status: "Claimed",
    reported_by: {
      name: "Neha Joshi",
      role: "Student",
      department: "Electrical Engineering (1st Year)",
      verified: true
    }
  },
  {
    id: 6,
    item_name: "Silver Fossil Chronograph Watch",
    item_description: "Stainless steel strap, dark blue dial with slight scratch at the 4 o'clock mark. Water resistant 50m model.",
    category: "Accessories",
    item_type: "Found",
    location: "Restroom near Canteen Block",
    date_lost_found: "2026-11-22",
    image: "static/images/placeholder.svg",
    status: "Active",
    reported_by: {
      name: "Campus Security Desk",
      role: "Security Officer",
      department: "Campus Safety & Surveillance",
      verified: true
    }
  },
  {
    id: 7,
    item_name: "Honda Bike Key with Red Lanyard",
    item_description: "Single bike key attached to a red 'Remove Before Flight' woven fabric keychain tag and small silver ring.",
    category: "Keys",
    item_type: "Lost",
    location: "Student Parking Lot (Sector 2)",
    date_lost_found: "2026-11-21",
    image: "static/images/placeholder.svg",
    status: "Active",
    reported_by: {
      name: "Karan Mehta",
      role: "Student",
      department: "Information Technology (4th Year)",
      verified: true
    }
  },
  {
    id: 8,
    item_name: "Milton Insulated Steel Flask (750ml)",
    item_description: "Matte olive green water bottle (750ml) with campus sports club vinyl sticker and black cap.",
    category: "Other",
    item_type: "Found",
    location: "Gymnasium Bench",
    date_lost_found: "2026-11-20",
    image: "static/images/placeholder.svg",
    status: "Resolved",
    reported_by: {
      name: "Deepak Saini",
      role: "Student",
      department: "Civil Engineering (3rd Year)",
      verified: true
    }
  }
];

if (typeof module !== "undefined" && module.exports) {
  module.exports = { MOCK_ITEMS };
}
