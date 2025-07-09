<div align="center">

# KIZAK Capstone Project

</div>

<p align="center">
    <img src="assets/logo.png" alt="KIZAK Logo" width="200"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-in%20progress-yellow" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
  <img src="https://img.shields.io/badge/build-Docker-blue" />
</p>


<div align="center">

***Your AI Guide to an IT Career***

</div>

KIZAK is an AI-powered learning assistant designed to guide users through their journey in the IT field. It builds personalized learning paths, recommends daily and weekly tasks, and supports users with a smart AI coach—all while keeping track of their skills and progress.

---

## 📋 Index

- [🚀 Features](#-features)  
- [🛠️ Tech Stack](#%EF%B8%8F-tech-stack)  
- [🗺️ Roadmap](#%EF%B8%8F-roadmap)  
- [⚡ Usage](#-usage)  
- [🐞 Open Issues and Contribution](#-open-issues-and-contribution)  
- [👥 Authors](#-authors)  
- [📄 License](#-license)

---

## 🚀 Features

- **Onboarding:** Personalized user profile creation with topic selection and skill assessment  
- **ML Agent:** AI-driven roadmap generation tailored to user goals and skills  
- **Personal Recommendations:** Daily/weekly curated courses and tasks from platforms like Coursera, Stepik, YouTube  
- **Resume Generation:** Automatic resume creation highlighting skills and projects  
- **AI Coach:** Interactive chatbot for Q&A, feedback, and interview simulation  
- **Integrations:** Connect with LinkedIn, GitHub, and support OAuth authentication  

---

## 🛠️ **Tech Stack**  

### **Backend**  
- **Flask**  🐍  - A **lightweight** Python web framework for building scalable APIs and backend services.
- **PostgreSQL** 🐘 - A **powerful**, open-source relational database with strong extensibility and SQL compliance.

### **Frontend**  
- **React** ⚛️ - **Fast and popular** JavaScript library for building dynamic, component-based user interfaces.
- **Next.js** ▲ - React framework for **server-side renderin**g, static sites, and **scalable web apps**.
- **Tailwind CSS** 🎨 - Utility-first CSS framework for **rapid UI development** with minimal custom CSS.
- **Redux** 🔄 - **State management** library for predictable global state in JavaScript apps.

### **ML / AI**  
- **LLaMA** 🦙 - Meta’s open-source large language model for **advanced NLP** tasks.
- **Transformers** 🤗 - Hugging Face’s library for state-of-the-art NLP models

---

## 🗺️ Roadmap

### 🧠 Week 1 – Project Planning
- 🟢 Finalize project idea and scope
- 🟢 Define user profiling structure
- 🟢 Choose tech stack

### 🧪 Week 2 – Prototyping
- 🟢 Gather and refine functional/non-functional requirements
- 🟢 Create UI/UX design prototype
- 🟢 Build basic frontend structure
- 🟢 Set up backend architecture and API contracts

### ⚙️ Week 3 – MVP v0
- 🟢 Implement core features (onboarding, roadmap engine)
- 🟢 Design and build initial database schema
- 🟢 Prepare working MVP demo

### 🧪 Week 4 – Testing & Deployment
- 🟡 Implement CI/CD pipeline
- 🟡 Add unit and integration tests
- 🟡 Deploy MVP to test/staging environment

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

## ⚡ Usage

### Requirements

**To run this project make sure that your docker-compose version is 2.24.0 or higher**
```
docker-compose -v
# Docker Compose version v2.24.0-desktop.1
```


### Deploy

First, clone the project:

```bash
git clone https://github.com/IU-Capstone-Project-2025/KIZAK
cd KIZAK
```

Now set up _.env_ file:

```bash
# Database configuration
DB_HOST=db
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_NAME=db

# CORS configuration
CORS_ORIGINS=http://localhost

# API configuration
API_HOST=backend
API_PORT=8000

# Frontend configuration
FRONTEND_HOST=frontend
FRONTEND_PORT=3000
FRONTEND_HOST_PORT=3000
```

Then build and run the project using Docker Compose:

```bash
docker-compose up --build
```

Visit [localhost:8000/docs](http://localhost:8000/docs) to access KIZAK API docs or [localhost:80](http://localhost) to see front part

## 🐞 Open Issues and Contribution

Check the [Issues](https://github.com/IU-Capstone-Project-2025/KIZAK/issues) tab to see current bugs, feature requests, and improvements.


### 👥 How to Contribute

We welcome contributions from the community! Here's how to get started:

1. **Fork the repository and clone it:**

   ```bash
   git clone https://github.com/IU-Capstone-Project-2025/KIZAK
   ```

2. **Create a new feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes, commit, and push:**

   ```bash
   git commit -m "Add: your detailed message here"
   git push origin feature/your-feature-name
   ```

4. **Open a pull request** with a clear description and reference any related issues.

✅ Before submitting a PR:

* Ensure your code is clean, linted, and tested
* Keep commits descriptive and scoped
* Link related issues (e.g., `Closes #123`)

</details>

---

## 👥 Authors

| Name                  | Email Address                                                                     | Responsibilities        |
| --------------------- | --------------------------------------------------------------------------------- | ----------------------- |
| Marsel Berheev (Lead) | [m.berheev@innopolis.university](mailto:m.berheev@innopolis.university)           | DevOps                  |
| Makar Egorov          | [m.egorov@innopolis.university](mailto:m.egorov@innopolis.university)             | Backend                 |
| Timur Farizunov       | [t.farizunov@innopolis.university](mailto:t.farizunov@innopolis.university)       | Frontend                |
| Maksim Malov          | [m.malov@innopolis.university](mailto:m.malov@innopolis.university)               | Backend                 |
| Sarmat Lutfullin      | [s.lutfullin@innopolis.university](mailto:s.lutfullin@innopolis.university)       | Frontend                |
| Ulyana Chaikovskaya   | [u.chaikouskaya@innopolis.university](mailto:u.chaikouskaya@innopolis.university) | ML                      |
| Kseniia Khudiakova    | [k.khudiakova@innopolis.university](mailto:k.khudiakova@innopolis.university)     | ML                      |

---

## 📄 License

This project is licensed under the [**MIT License**](LICENSE).
