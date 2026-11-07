
import random

QUESTION_BANK = {

    "python": {
        "beginner": [
            "What are the main features of Python?",
            "What are Python's built-in data types?",
            "What is the difference between a list and a tuple?",
            "What is the difference between break and continue?",
            "How do you define and call a function in Python?",
            "What is the difference between == and is?",
            "What are mutable and immutable objects?",
            "How do you handle exceptions using try and except?"
        ],
        "intermediate": [
            "What are decorators in Python and when would you use them?",
            "How do generators work in Python?",
            "What is the difference between shallow copy and deep copy?",
            "What are *args and **kwargs?",
            "How does list comprehension work?",
            "What is the difference between an iterator and an iterable?",
            "How do Python modules and packages work?",
            "What are lambda functions and where are they useful?"
        ],
        "advanced": [
            "What is the Global Interpreter Lock (GIL) in Python?",
            "How does Python's garbage collection work?",
            "How does Python manage memory internally?",
            "How does multiple inheritance work in Python?",
            "How would you optimize a memory-intensive Python application?",
            "What is metaprogramming in Python?",
            "How do multiprocessing and multithreading differ in Python?",
            "How would you profile and optimize a slow Python application?"
        ]
    },

    "sql": {
        "beginner": [
            "What is SQL?",
            "What is the difference between primary key and foreign key?",
            "What is the difference between DELETE, DROP and TRUNCATE?",
            "What is a database table?",
            "What is the purpose of the SELECT statement?",
            "What is the difference between WHERE and ORDER BY?",
            "What are NULL values in SQL?",
            "What is the purpose of the DISTINCT keyword?"
        ],
        "intermediate": [
            "What is the difference between INNER JOIN and LEFT JOIN?",
            "What is the difference between GROUP BY and HAVING?",
            "What are subqueries in SQL?",
            "What are aggregate functions in SQL?",
            "What is database normalization?",
            "What is the difference between UNION and UNION ALL?",
            "How do you find duplicate records in a table?",
            "What are indexes and why are they used?"
        ],
        "advanced": [
            "What are database transactions and ACID properties?",
            "How do indexes improve query performance?",
            "What are window functions in SQL?",
            "How would you optimize a slow SQL query?",
            "What is the difference between clustered and non-clustered indexes?",
            "What are database isolation levels?",
            "How do you identify and resolve database deadlocks?",
            "How would you design a database for a high-traffic application?"
        ]
    },

    "dsa": {
        "beginner": [
            "What is a data structure?",
            "What is the difference between an array and a linked list?",
            "What is a stack?",
            "What is a queue?",
            "What is linear search?",
            "What is binary search?",
            "What is the time complexity of accessing an array element?",
            "What is recursion?"
        ],
        "intermediate": [
            "How does a hash table work?",
            "What is the difference between BFS and DFS?",
            "How does merge sort work?",
            "What is the time complexity of quicksort?",
            "How can two pointers solve array problems?",
            "What is the sliding window technique?",
            "How do you detect a cycle in a linked list?",
            "What is the difference between a binary tree and a binary search tree?"
        ],
        "advanced": [
            "How does Dijkstra's shortest path algorithm work?",
            "What is dynamic programming and when should it be used?",
            "How would you optimize a solution with O(n squared) complexity?",
            "What is the difference between a segment tree and a Fenwick tree?",
            "How does a disjoint set union data structure work?",
            "What are topological sorting and its applications?",
            "How would you solve a complex graph optimization problem?",
            "How do you analyze amortized time complexity?"
        ]
    },

    "oops": {
        "beginner": [
            "What is object-oriented programming?",
            "What is a class and an object?",
            "What is inheritance?",
            "What is encapsulation?",
            "What is polymorphism?",
            "What is abstraction?",
            "What is a constructor?",
            "What is the difference between a class variable and an instance variable?"
        ],
        "intermediate": [
            "What is method overriding?",
            "What is method overloading?",
            "What is the difference between abstraction and encapsulation?",
            "What is multiple inheritance?",
            "What is the difference between composition and inheritance?",
            "What are access modifiers?",
            "What is the difference between an abstract class and an interface?",
            "What is the purpose of the super() function?"
        ],
        "advanced": [
            "What are SOLID principles?",
            "How does method resolution order work in multiple inheritance?",
            "What are design patterns and why are they useful?",
            "Explain dependency injection with an example.",
            "What is the Liskov Substitution Principle?",
            "How would you design loosely coupled object-oriented software?",
            "What is the difference between composition and aggregation?",
            "How would you refactor a class with too many responsibilities?"
        ]
    },

    "dbms": {
        "beginner": [
            "What is a DBMS?",
            "What is the difference between DBMS and RDBMS?",
            "What is a primary key?",
            "What is a foreign key?",
            "What is database normalization?",
            "What is a database schema?",
            "What is a relationship in a database?",
            "What are the different types of database relationships?"
        ],
        "intermediate": [
            "Explain the first, second and third normal forms.",
            "What is the difference between candidate key and super key?",
            "What is an ER diagram?",
            "What is referential integrity?",
            "What is the difference between a view and a table?",
            "What are database indexes?",
            "What is a transaction?",
            "What is the difference between horizontal and vertical partitioning?"
        ],
        "advanced": [
            "Explain ACID properties with practical examples.",
            "What are database concurrency control techniques?",
            "What is two-phase locking?",
            "How do database recovery mechanisms work?",
            "What is database sharding?",
            "How would you handle database scalability?",
            "What are distributed transactions?",
            "How do isolation levels affect concurrent transactions?"
        ]
    },

    "operating systems": {
        "beginner": [
            "What is an operating system?",
            "What is a process?",
            "What is a thread?",
            "What is multitasking?",
            "What is virtual memory?",
            "What is a deadlock?",
            "What is the difference between RAM and ROM?",
            "What is CPU scheduling?"
        ],
        "intermediate": [
            "What is the difference between a process and a thread?",
            "Explain the different CPU scheduling algorithms.",
            "What are the four necessary conditions for deadlock?",
            "What is paging in operating systems?",
            "What is the difference between paging and segmentation?",
            "What is context switching?",
            "What is a semaphore?",
            "What is the difference between a mutex and a semaphore?"
        ],
        "advanced": [
            "How does virtual memory work internally?",
            "Explain deadlock prevention, avoidance and detection.",
            "How does the copy-on-write mechanism work?",
            "What is the difference between monolithic and microkernel architecture?",
            "How would you diagnose a memory leak at the operating system level?",
            "What is thrashing and how can it be prevented?",
            "How do modern operating systems handle concurrency?",
            "What is the role of kernel mode and user mode?"
        ]
    },

    "computer networks": {
        "beginner": [
            "What is a computer network?",
            "What is an IP address?",
            "What is the difference between LAN and WAN?",
            "What is the OSI model?",
            "What is a router?",
            "What is DNS?",
            "What is the difference between HTTP and HTTPS?",
            "What is a MAC address?"
        ],
        "intermediate": [
            "Explain the seven layers of the OSI model.",
            "What is the difference between TCP and UDP?",
            "How does the DNS resolution process work?",
            "What is the difference between a switch and a router?",
            "What is subnetting?",
            "What is the TCP three-way handshake?",
            "What is DHCP?",
            "What happens when you enter a URL in a browser?"
        ],
        "advanced": [
            "How does TLS establish a secure connection?",
            "How does TCP congestion control work?",
            "What is the difference between HTTP/1.1, HTTP/2 and HTTP/3?",
            "How would you troubleshoot intermittent network latency?",
            "What is a reverse proxy and how does it work?",
            "How does load balancing work at the network level?",
            "What are BGP and its role in internet routing?",
            "How would you design a highly available network architecture?"
        ]
    },

    "html css": {
        "beginner": [
            "What is HTML?",
            "What is CSS?",
            "What are HTML semantic elements?",
            "What is the difference between id and class?",
            "What is the CSS box model?",
            "What is the purpose of the div element?",
            "What are inline and block elements?",
            "How do you add a link and an image in HTML?"
        ],
        "intermediate": [
            "What is the difference between Flexbox and CSS Grid?",
            "What are CSS pseudo-classes?",
            "What is responsive web design?",
            "How does CSS specificity work?",
            "What are media queries?",
            "What is the difference between relative, absolute and fixed positioning?",
            "What is the difference between localStorage and sessionStorage?",
            "How do you improve the accessibility of an HTML page?"
        ],
        "advanced": [
            "How would you optimize the rendering performance of a complex webpage?",
            "How does the browser's rendering pipeline work?",
            "What is CSS containment?",
            "How would you structure CSS for a large application?",
            "What are critical rendering path optimizations?",
            "How do you prevent layout shifts in a webpage?",
            "How would you implement a scalable responsive design system?",
            "How do you optimize web accessibility for a large application?"
        ]
    },

    "javascript": {
        "beginner": [
            "What is JavaScript?",
            "What is the difference between var, let and const?",
            "What are JavaScript data types?",
            "What is a function in JavaScript?",
            "What is an array?",
            "What is the difference between == and ===?",
            "What is the DOM?",
            "What is an event in JavaScript?"
        ],
        "intermediate": [
            "What is closure in JavaScript?",
            "What is the difference between null and undefined?",
            "How does event bubbling work?",
            "What are promises?",
            "What is async and await?",
            "What is hoisting?",
            "What is the difference between map(), filter() and reduce()?",
            "What is the event loop?"
        ],
        "advanced": [
            "Explain the JavaScript event loop and microtask queue.",
            "How does prototypal inheritance work?",
            "What are memory leaks in JavaScript and how do you prevent them?",
            "How does the JavaScript engine optimize code execution?",
            "What are web workers and when would you use them?",
            "How would you optimize a large JavaScript application?",
            "What are generators and iterators in JavaScript?",
            "How does garbage collection work in JavaScript?"
        ]
    },

    "react": {
        "beginner": [
            "What is React?",
            "What is a React component?",
            "What is JSX?",
            "What are props in React?",
            "What is state in React?",
            "What is the purpose of the useState hook?",
            "What is the virtual DOM?",
            "What is conditional rendering?"
        ],
        "intermediate": [
            "What is the useEffect hook?",
            "What is the difference between props and state?",
            "What are controlled components?",
            "What is prop drilling?",
            "What is React Context?",
            "What are React keys and why are they important?",
            "How does React Router work?",
            "What is the purpose of useMemo and useCallback?"
        ],
        "advanced": [
            "How does React reconciliation work?",
            "How would you optimize unnecessary component re-renders?",
            "What is code splitting in React?",
            "How does server-side rendering differ from client-side rendering?",
            "How would you manage complex application state?",
            "What are React Server Components?",
            "How do you identify performance bottlenecks in React?",
            "How would you architect a large-scale React application?"
        ]
    },

    "fastapi": {
        "beginner": [
            "What is FastAPI?",
            "What is an API endpoint?",
            "What is the purpose of a Pydantic model?",
            "What is the difference between GET and POST?",
            "What is path parameter in FastAPI?",
            "What is query parameter in FastAPI?",
            "What is automatic API documentation?",
            "How do you run a FastAPI application?"
        ],
        "intermediate": [
            "What is dependency injection in FastAPI?",
            "How does request validation work in FastAPI?",
            "How do you implement JWT authentication?",
            "What is the purpose of APIRouter?",
            "How does asynchronous programming work in FastAPI?",
            "How do you handle file uploads?",
            "How do you connect FastAPI to PostgreSQL?",
            "How do you handle exceptions in FastAPI?"
        ],
        "advanced": [
            "How would you structure a large FastAPI application?",
            "How do you secure a FastAPI application against common attacks?",
            "How would you implement role-based access control?",
            "How do you optimize database operations in FastAPI?",
            "How would you manage background tasks at scale?",
            "How would you implement rate limiting in FastAPI?",
            "How would you deploy FastAPI using multiple workers?",
            "How would you design a scalable asynchronous API?"
        ]
    },

    "django": {
        "beginner": [
            "What is Django?",
            "What is the Django MVT architecture?",
            "What is a Django model?",
            "What is a Django view?",
            "What is a Django template?",
            "What is the Django admin panel?",
            "What is a Django app?",
            "What is the purpose of manage.py?"
        ],
        "intermediate": [
            "What are Django migrations?",
            "What is Django ORM?",
            "What is middleware in Django?",
            "How does Django authentication work?",
            "What is the difference between select_related and prefetch_related?",
            "How do you create REST APIs using Django REST Framework?",
            "What are class-based views?",
            "How does Django handle form validation?"
        ],
        "advanced": [
            "How would you optimize a Django application with slow database queries?",
            "How does Django handle CSRF protection?",
            "How would you design a scalable Django architecture?",
            "How do Django signals work and when should they be avoided?",
            "How would you implement caching in Django?",
            "How would you secure a production Django application?",
            "How do you handle asynchronous tasks in Django?",
            "How would you optimize Django ORM performance?"
        ]
    },

    "machine learning": {
        "beginner": [
            "What is machine learning?",
            "What is supervised learning?",
            "What is unsupervised learning?",
            "What is the difference between classification and regression?",
            "What is a training dataset?",
            "What is a feature in machine learning?",
            "What is a machine learning model?",
            "What is overfitting?"
        ],
        "intermediate": [
            "What is the bias-variance tradeoff?",
            "What is cross-validation?",
            "How do you handle missing values in a dataset?",
            "What is feature scaling?",
            "What is regularization?",
            "How do precision and recall differ?",
            "What is a confusion matrix?",
            "How do you handle imbalanced datasets?"
        ],
        "advanced": [
            "How would you prevent data leakage in a machine learning pipeline?",
            "How would you detect model drift?",
            "How do you choose between different model architectures?",
            "How would you optimize inference latency?",
            "What is the difference between bagging and boosting?",
            "How would you deploy and monitor an ML model in production?",
            "How do you explain model predictions using SHAP or LIME?",
            "How would you design a reproducible machine learning pipeline?"
        ]
    },

    "generative ai": {
        "beginner": [
            "What is Generative AI?",
            "What is a large language model?",
            "What is a prompt?",
            "What is the difference between AI and Generative AI?",
            "What is a token in a language model?",
            "What is prompt engineering?",
            "What are some applications of Generative AI?",
            "What is an AI hallucination?"
        ],
        "intermediate": [
            "What is Retrieval-Augmented Generation (RAG)?",
            "What are embeddings in Generative AI?",
            "What is a vector database?",
            "What is prompt chaining?",
            "What is the difference between fine-tuning and prompting?",
            "How does semantic search work?",
            "What is an AI agent?",
            "How do you evaluate the quality of LLM responses?"
        ],
        "advanced": [
            "How would you design a production-ready RAG pipeline?",
            "How would you reduce hallucinations in an LLM application?",
            "How do you optimize token usage and inference cost?",
            "How would you evaluate an LLM-powered application?",
            "How do multi-agent systems coordinate tasks?",
            "How would you secure an LLM application against prompt injection?",
            "How would you design a scalable AI agent architecture?",
            "How would you implement hybrid search in a RAG system?"
        ]
    },

    "system design": {
        "beginner": [
            "What is system design?",
            "What is the difference between monolithic and microservices architecture?",
            "What is a client-server architecture?",
            "What is load balancing?",
            "What is caching?",
            "What is a database in system design?",
            "What is horizontal scaling?",
            "What is an API gateway?"
        ],
        "intermediate": [
            "How would you design a URL shortening service?",
            "What is the difference between horizontal and vertical scaling?",
            "What is database replication?",
            "What is database sharding?",
            "How does a message queue work?",
            "What is the CAP theorem?",
            "How does caching improve application performance?",
            "What is eventual consistency?"
        ],
        "advanced": [
            "How would you design a highly available distributed system?",
            "How would you design a scalable notification service?",
            "How would you handle distributed transactions?",
            "How would you design a system supporting millions of concurrent users?",
            "How do you prevent cascading failures in microservices?",
            "How would you design a fault-tolerant payment system?",
            "How would you ensure consistency in a distributed database?",
            "How would you design an event-driven architecture?"
        ]
    },

    "general": {
        "beginner": [
            "Tell me about yourself.",
            "Why do you want to become a software developer?",
            "What are your technical strengths?",
            "What is your favorite programming language and why?",
            "Describe a project you have worked on.",
            "How do you approach learning a new technology?",
            "What is the difference between a bug and an error?",
            "How do you approach solving a programming problem?"
        ],
        "intermediate": [
            "Describe a challenging technical problem you solved.",
            "How do you debug an application?",
            "How do you manage your time when working on multiple tasks?",
            "How do you handle feedback during code reviews?",
            "How do you approach learning an unfamiliar codebase?",
            "Describe how you would work with a team on a software project.",
            "How do you ensure code quality?",
            "How would you explain a technical concept to a non-technical person?"
        ],
        "advanced": [
            "Describe a technical decision you made and its trade-offs.",
            "How would you handle a critical production issue?",
            "How would you improve a poorly maintained codebase?",
            "How do you balance delivery speed with software quality?",
            "How would you handle disagreement about a technical design?",
            "How would you mentor a junior developer?",
            "How would you approach a project with unclear requirements?",
            "How would you identify technical debt and prioritize its resolution?"
        ]
    }
}


# =====================================================
# ROLE-WISE QUESTION BANK
# Each role also has separate difficulty levels
# =====================================================

ROLE_QUESTIONS = {

    "python developer": {
        "beginner": [
            "How do you install and use Python packages?",
            "How do you read and write files in Python?",
            "What is the purpose of Python's pip tool?"
        ],
        "intermediate": [
            "How would you organize a maintainable Python project?",
            "How do you write unit tests for Python functions?",
            "How would you handle configuration and environment variables in Python?"
        ],
        "advanced": [
            "How would you design a reusable Python library?",
            "How would you profile a Python application to find performance bottlenecks?",
            "How would you design a robust error-handling strategy for a Python application?"
        ]
    },

    "backend developer": {
        "beginner": [
            "What is the responsibility of a backend developer?",
            "What is the request-response cycle?",
            "What is the purpose of an HTTP status code?"
        ],
        "intermediate": [
            "How would you implement authentication in a REST API?",
            "How do you validate incoming API requests?",
            "How would you handle database errors in a backend service?"
        ],
        "advanced": [
            "How would you design a scalable backend architecture?",
            "How would you handle high traffic in a backend application?",
            "How would you design fault tolerance in distributed backend services?"
        ]
    },

    "software developer": {
        "beginner": [
            "What are the main stages of the software development life cycle?",
            "What is debugging?",
            "What is the difference between a compiler and an interpreter?"
        ],
        "intermediate": [
            "What are the SOLID principles?",
            "What is the difference between unit and integration testing?",
            "How does version control help software development?"
        ],
        "advanced": [
            "How would you design software for scalability and maintainability?",
            "How would you identify and resolve performance bottlenecks?",
            "How would you plan a safe migration of a large software system?"
        ]
    },

    "data analyst": {
        "beginner": [
            "What is data analysis?",
            "What is the purpose of data cleaning?",
            "What is the difference between a row and a column in a dataset?"
        ],
        "intermediate": [
            "How would you identify outliers in a dataset?",
            "How do you use SQL to summarize business data?",
            "How would you communicate insights using a dashboard?"
        ],
        "advanced": [
            "How would you design a reliable data validation pipeline?",
            "How would you analyze a large dataset efficiently?",
            "How would you communicate statistical findings to business stakeholders?"
        ]
    },

    "data scientist": {
        "beginner": [
            "What is the difference between AI, ML and deep learning?",
            "What is a dataset?",
            "What is supervised learning?"
        ],
        "intermediate": [
            "What is the bias-variance tradeoff?",
            "How do you handle imbalanced datasets?",
            "What is cross-validation?"
        ],
        "advanced": [
            "How would you detect and prevent data leakage?",
            "How would you deploy and monitor a machine learning model?",
            "How would you select a model for a complex prediction problem?"
        ]
    },

    "ai/ml engineer": {
        "beginner": [
            "What is machine learning?",
            "What is the difference between classification and regression?",
            "What is a neural network?"
        ],
        "intermediate": [
            "What is gradient descent?",
            "How do you evaluate a machine learning model?",
            "What is feature engineering?"
        ],
        "advanced": [
            "How would you optimize the inference latency of an ML model?",
            "How would you design an end-to-end machine learning pipeline?",
            "How would you monitor model drift in production?"
        ]
    },

    "frontend developer": {
        "beginner": [
            "What is the purpose of HTML?",
            "What is CSS used for?",
            "What is JavaScript?"
        ],
        "intermediate": [
            "What is event bubbling in JavaScript?",
            "What is the difference between Flexbox and CSS Grid?",
            "How does asynchronous JavaScript work?"
        ],
        "advanced": [
            "How would you optimize a large frontend application?",
            "How would you manage complex application state?",
            "How would you improve frontend accessibility?"
        ]
    },

    "full stack developer": {
        "beginner": [
            "What is the difference between frontend and backend?",
            "What is the purpose of a database?",
            "What is an HTTP request?"
        ],
        "intermediate": [
            "How does a frontend application communicate with a backend API?",
            "How do you implement authentication in a full-stack application?",
            "How would you handle form validation on frontend and backend?"
        ],
        "advanced": [
            "How would you design a scalable full-stack application?",
            "How would you secure communication between frontend and backend?",
            "How would you manage caching across a full-stack application?"
        ]
    },

    "java developer": {
        "beginner": [
            "What are the main features of Java?",
            "What is the difference between JDK, JRE and JVM?",
            "What is a class in Java?"
        ],
        "intermediate": [
            "What is the difference between an interface and an abstract class?",
            "How does exception handling work in Java?",
            "What is the Java Collections Framework?"
        ],
        "advanced": [
            "How does garbage collection work in Java?",
            "How does multithreading work in Java?",
            "How would you diagnose a memory leak in a Java application?"
        ]
    }
}


# =====================================================
# QUESTION GENERATION FUNCTION
# =====================================================

def get_questions(
    topic: str,
    role: str = "",
    experience_level: str = "Beginner",
    count: int = 5
) -> list[str]:

    topic_key = topic.strip().lower()
    role_key = role.strip().lower()
    level_key = experience_level.strip().lower()

    # Only select questions from the requested difficulty
    topic_levels = QUESTION_BANK.get(
        topic_key,
        QUESTION_BANK["general"]
    )

    topic_questions = topic_levels.get(
        level_key,
        topic_levels["beginner"]
    )

    # Add role-specific questions from the SAME difficulty
    role_levels = ROLE_QUESTIONS.get(role_key, {})
    role_questions = role_levels.get(level_key, [])

    # Combine without duplicate questions
    combined_questions = list(
        dict.fromkeys(topic_questions + role_questions)
    )

    # Randomly select the requested number
    selected_count = min(count, len(combined_questions))

    return random.sample(combined_questions, selected_count)
