<div align="center">

# KIZAK Capstone Project

</div>


<p align="center">
    <img src="assets/logo.png" alt="KIZAK Logo" width="200"/>
</p>

<div align="center">

***Your AI Guide to an IT Career***

</div>


KIZAK is an AI-powered learning assistant designed to guide users through their journey in the IT field. It builds personalized learning paths, recommends daily and weekly tasks, and supports users with a smart AI coach—all while keeping track of their skills and progress.

---

## 📋 Index

- [🚀 Features](#🚀-features)  
- [🛠️ Tech Stack](#🛠️-tech-stack)  
- [🗺️ Roadmap](#🗺️-roadmap)  
- [⚙️ Usage](#usage)  
- [🐞 Open Issues and Contribution](#open-issues-and-contribution)  
- [👥 Authors](#authors)  
- [📄 License](#license)  

---

## 🚀 Features

- **Onboarding:** Personalized user profile creation with topic selection and skill assessment  
- **ML Agent:** AI-driven roadmap generation tailored to user goals and skills  
- **Personal Recommendations:** Daily/weekly curated courses and tasks from platforms like Coursera, Stepik, YouTube  
- **Resume Generation:** Automatic resume creation highlighting skills and projects  
- **AI Coach:** Interactive chatbot for Q&A, feedback, and interview simulation  
- **Integrations:** Connect with LinkedIn, GitHub, and support OAuth authentication  

---

## 🛠️ Tech Stack
TODO 

---

## 🗺️ Roadmap

### 🧠 Week 1 – Project Planning
- 🟢 Finalize project idea and scope
- 🟢 Define user profiling structure
- 🟢 Choose tech stack

### 🧪 Week 2 – Prototyping
- 🟡 Gather and refine functional/non-functional requirements
- 🟡 Create UI/UX design prototype
- 🟡 Build basic frontend structure
- 🟡 Set up backend architecture and API contracts

### ⚙️ Week 3 – MVP v0
- 🔴 Implement core features (onboarding, roadmap engine)
- 🔴 Design and build initial database schema
- 🔴 Prepare working MVP demo

### 🧪 Week 4 – Testing & Deployment
- 🔴 Implement CI/CD pipeline
- 🔴 Add unit and integration tests
- 🔴 Deploy MVP to test/staging environment

### 🎨 Week 5 – Polishing
- 🔴 Gather feedback from initial users/stakeholders
- 🔴 Refactor codebase and improve UX/UI
- 🔴 Fix bugs and optimize performance

### 🧾 Week 6 – Finalization
- 🔴 Finalize all project components
- 🔴 Prepare project documentation
- 🔴 Build and design presentation materials

### 🎤 Week 7 – Final Presentation
- 🔴 Rehearse and deliver final presentation
- 🔴 Submit final deliverables

---

## ⚙️ Usage

First of all, get our project

```bash
git clone https://github.com/LowIQCoder/KIZAK_Capstone
cd KIZAK_Capstone
```

Now you need to create the following **.env** file

```bash
# Deploy
HOST_BASE="localhost"

# Backend
API_PORT="8000"

# Frontend
FRONT_PORT="80"

# Database
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="mydatabase"
DB_USER="myuser"
DB_PASSWORD="mypassword"
```

Now build and run our project with use of **docker compose**

```bash
docker-compose up --build
```

Now access and test **KIZAK** on [localhost](http://localhost:80)

---

## 🐞 Open Issues and Contribution

Check the [Issues](https://github.com/yourusername/kizak/issues) tab to see current bugs, feature requests, and improvements.

### 👥 Want to Contribute?

We welcome contributions from the community! Here's how you can help:

Fork the repository and clone it
```bash
git clone https://github.com/yourusername/kizak.git
```

Create a new branch 
```bash
git checkout -b feature/your-feature-name
```
Add your feature and push
```bash
git commit -m "Add: your detailed message here"
git push origin feature/your-feature-name
```

Finally, open a *pull request*, describe your changes clearly and link to any related issues

Before submitting a PR:
* Ensure code is formatted and linted
* Test your changes locally
* Reference relevant issue numbers if applicable

---

## 👥 Authors

| Team Member           | Email Address                      | Responsibilities        |
|-----------------------|----------------------------------|-------------------------|
| Marsel Berheev (Lead) | m.berheev@innopolis.univesity    | DevOps                  |
| Makar Egorov          | m.egorov@innopolis.univesity     | Backend                 |
| Timur Farizunov       | t.farizunov@innopolis.univesity  | Frontend                |
| Maksim Malov          | m.malov@innopolis.univesity      | Backend                 |
| Sarmat Lutfullin      | s.lutfullin@innopolis.univesity  | Frontend                |
| Ulyana Chaikovskaya   | u.chaikouskaya@innopolis.univesity | [Responsibilities TBD] |
| Kseniia Khudiakova    | k.khudiakova@innopolis.univesity | ML                      |



---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

