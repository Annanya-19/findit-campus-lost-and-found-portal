# FindIt – Campus Lost & Found Portal

A simple web-based platform that helps students report lost belongings, find items reported by others, and claim their belongings within the college campus.

## 🌐 Live Website

[**Visit FindIt**](https://findit-campus-lost-and-found-portal-production.up.railway.app)

## About the Project
Losing something on campus is quite common. It could be an ID card, wallet, set of keys, earphones, or even a notebook. Usually, students depend on word of mouth or class groups to find their missing belongings, which can make the process difficult.

**FindIt** was developed to make this process easier by bringing lost and found reports together in one place.
Students can report lost or found items, browse existing listings, search using keywords and filters, and submit claims for items they recognise. An admin can manage reported items and review submitted claims.
## Features
### Student Features
- Register and log in using a student account.
- Report lost or found belongings.
- Upload images of reported items.
- Browse all reported items.
- Search items by keywords.
- Filter listings by category and item type.
- View item details, including location and date.
- Submit claims with a message.
- Track the status of submitted claims.
### Admin Features
- Separate admin login.
- View dashboard statistics.
- View all reported items.
- Search and manage listings.
- View pending claims.
- Approve or reject claims.
- Mark items as resolved.
- Delete reported items when required.
## Tech Stack
| Technology | Purpose |
|---|---|
| Python | Backend development |
| Flask | Web framework and API handling |
| SQLite | Database management |
| HTML | Page structure |
| CSS | Styling and layout |
| JavaScript | Frontend functionality |
| Gunicorn | Production application server |
| Railway | Hosting and deployment |
| Git & GitHub | Version control |
## How It Works
1. A student creates an account and logs in.
2. The student reports an item as either Lost or Found.
3. The report is saved in the database along with its details and optional image.
4. Other students can browse and search the available listings.
5. If someone recognises an item, they can submit a claim.
6. The admin reviews the claim and approves or rejects it.
7. Once approved, the item is marked as resolved.
## Deployment
The application is hosted on Railway and connected to the GitHub repository for deployment.
**Live URL:**  

https://findit-campus-lost-and-found-portal-production.up.railway.app
## Developed As

**FindIt – Campus Lost & Found Management System**

Developed as part of a Software Engineering CCA project.

The idea behind FindIt is simple: make it easier for students to report, search for, and recover belongings within their campus.
