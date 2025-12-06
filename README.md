# Doggiedoo

A lightweight REST API for tracking dog activities including walks, bathroom breaks, and sickness routines. Built with Python and the Falcon framework, deployed to AWS Elastic Beanstalk.

## Features

- Record dog activities with timestamps
- Retrieve history of all recorded actions
- Clear all activity records
- CORS-enabled for cross-origin requests
- Lightweight SQLite database storage

## Tech Stack

- **Language:** Python 3.7+
- **Framework:** [Falcon](https://falcon.readthedocs.io/) - High-performance REST API framework
- **Server:** [Gunicorn](https://gunicorn.org/) - WSGI HTTP Server
- **Database:** SQLite
- **Infrastructure:** AWS Elastic Beanstalk
- **IaC:** Terraform
- **CI/CD:** Jenkins

## Project Structure

```
doggiedoo/
├── api/
│   ├── __init__.py
│   └── app.py              # Main Falcon application and route handlers
├── helpers/
│   ├── __init__.py
│   ├── db_helper.py        # Database operations class
│   └── dog_actions.db      # SQLite database file
├── JenkinsFile             # Jenkins CI/CD pipeline configuration
├── main.tf                 # Terraform configuration for AWS
├── gunicorn.config.py      # Gunicorn server configuration
├── requirements.txt        # Python dependencies
└── README.md
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jfavaron/doggiedoo.git
   cd doggiedoo
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development

```bash
gunicorn api.app:application
```

The API will be available at `http://localhost:8000`.

### With Custom Configuration

```bash
gunicorn api.app:application -c gunicorn.config.py
```

### Specify Host and Port

```bash
gunicorn api.app:application -b 0.0.0.0:5000
```

## API Documentation

### Base URL

```
http://localhost:8000
```

### Endpoints

#### Save Action

Records a new dog activity.

- **URL:** `/save_action`
- **Method:** `POST`
- **Content-Type:** `application/json`

**Request Body:**

| Field | Type | Description |
|-------|------|-------------|
| `dog` | string | Name of the dog |
| `action` | string | Type of activity (e.g., "walk", "bathroom", "sick") |
| `timestamp` | string | When the action occurred |

**Example Request:**

```bash
curl -X POST http://localhost:8000/save_action \
  -H "Content-Type: application/json" \
  -d '{"dog": "Buddy", "action": "walk", "timestamp": "2025-12-06 10:30:00"}'
```

**Example Response:**

```json
{
  "dog": "Buddy",
  "action": "walk",
  "id": 1
}
```

---

#### List Actions

Retrieves all recorded dog activities.

- **URL:** `/list_actions`
- **Method:** `GET`

**Example Request:**

```bash
curl http://localhost:8000/list_actions
```

**Example Response:**

```json
[
  [1, "Buddy", "walk", "2025-12-06 10:30:00"],
  [2, "Max", "bathroom", "2025-12-06 11:00:00"],
  [3, "Buddy", "sick", "2025-12-06 14:15:00"]
]
```

Response format: `[id, name, action, timestamp]`

---

#### Delete Actions

Deletes all recorded activities.

- **URL:** `/delete_actions`
- **Method:** `POST`

**Example Request:**

```bash
curl -X POST http://localhost:8000/delete_actions
```

**Example Response:**

```
yay
```

## Database Schema

The application uses SQLite with a single `actions` table:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `name` | TEXT | Dog's name |
| `action` | TEXT | Activity type |
| `timestamp` | TEXT | When the action occurred |

## Deployment

### AWS Elastic Beanstalk

The application is configured for deployment to AWS Elastic Beanstalk using Terraform and Jenkins.

#### Prerequisites for Deployment

- AWS account with appropriate permissions
- Jenkins server with AWS credentials configured
- Terraform installed

#### Jenkins Pipeline

The `JenkinsFile` defines a pipeline that:

1. Cleans the workspace
2. Checks out the source code
3. Installs Terraform and AWS CLI
4. Runs `terraform init` and `terraform apply`

#### Manual Terraform Deployment

```bash
# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply
```

## Configuration

### Gunicorn

The `gunicorn.config.py` file configures logging:

```python
accesslog = 'gunicorn.log'
errorlog = 'gunicorn.error.log'
```

### Environment Variables (for Jenkins deployment)

| Variable | Description |
|----------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_DEFAULT_REGION` | AWS region (default: us-east-1) |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).
