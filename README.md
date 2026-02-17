Movie Rental SaaS API

A production-ready Movie Rental REST API built with Django REST Framework, PostgreSQL, Redis, and Docker. 
Includes role-based authentication, transaction-safe inventory management, analytics, caching, and CI automation.

Tech Stack
•	Python
•	Django
•	Django REST Framework
•	PostgreSQL
•	Redis
•	Docker
•	GitHub Actions

Key Features
•	Role-based authentication (Admin / Customer)
•	Safe inventory management using database transactions
•	Row-level locking with select_for_update
•	Filtering, search, ordering, pagination
•	Revenue analytics endpoint
•	Redis caching
•	PostgreSQL database
•	CI pipeline with GitHub Actions
•	Dockerized deployment

Architecture Decisions
•	Used PostgreSQL for production-grade reliability
•	Used transactions to prevent race conditions
•	Used database-level constraints for data integrity
•	Separated validation and business logic
•	Added CI for automated testing
