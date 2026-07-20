# Docker & Kubernetes Quiz

A web-based quiz application to test your Docker and Kubernetes command-line knowledge. This quiz features 20 command completion questions ranging from easy to hard difficulty.

## Features

- **20 Questions**: Progressive difficulty from Easy to Hard
- **Command Completion**: Complete Docker and Kubernetes commands
- **Real-time Scoring**: Track your score as you progress
- **Hints**: Each question includes a helpful hint
- **Beautiful UI**: Modern, responsive web interface
- **Docker Ready**: Run easily with Docker or Docker Compose
- **Detailed Results**: Review all answers at the end

## Questions Breakdown

- **Easy (Questions 1-5)**: Basic Docker commands
- **Easy-Medium (Questions 6-10)**: Basic Kubernetes commands
- **Medium (Questions 11-15)**: Intermediate Docker and K8s operations
- **Medium-Hard (Questions 16-18)**: Advanced operations
- **Hard (Questions 19-20)**: Expert-level commands

## Quick Start with Docker

### Using Docker Compose (Recommended)

1. Navigate to the quiz directory:
```bash
cd quiz
```

2. Run the quiz:
```bash
docker-compose up -d
```

3. Open your browser and visit:
```
http://localhost:5000
```

4. To stop the quiz:
```bash
docker-compose down
```

### Using Docker directly

1. Build the Docker image:
```bash
docker build -t docker-k8s-quiz .
```

2. Run the container:
```bash
docker run -p 5000:5000 docker-k8s-quiz
```

3. Open your browser and visit:
```
http://localhost:5000
```

4. To stop the container:
```bash
docker stop <container-id>
```

## Running Locally (Without Docker)

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

1. Navigate to the quiz directory:
```bash
cd quiz
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit:
```
http://localhost:5000
```

## How to Use

1. **Start the Quiz**: Click "Start Quiz" on the home page
2. **Answer Questions**: Type the complete command for each question
3. **Get Feedback**: See immediate feedback after each answer
4. **View Results**: At the end, see your score and review all answers
5. **Try Again**: Restart the quiz to improve your score

## Scoring

- **20/20**: Perfect! You are a Docker & Kubernetes master! 🏆
- **16-19**: Excellent! You have strong knowledge! 🌟
- **12-15**: Good job! Keep practicing! 👍
- **8-11**: Not bad! Room for improvement! 📚
- **0-7**: Keep studying! You'll get there! 💪

## Sample Questions

**Easy**: What command is used to list all running Docker containers?
- Answer: `docker ps`

**Medium**: What command executes a command inside a running Docker container?
- Answer: `docker exec`

**Hard**: What command port-forwards a local port to a Kubernetes pod?
- Answer: `kubectl port-forward`

## Project Structure

```
quiz/
├── app.py                 # Flask application with quiz logic
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
├── templates/
│   └── index.html        # Quiz UI template
└── README.md            # This file
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker, Docker Compose
- **Port**: 5000

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, you can change the port in `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Use port 8080 instead
```

### Container Won't Start
Check the logs:
```bash
docker-compose logs
```

### Can't Access the Quiz
1. Verify the container is running:
```bash
docker ps
```

2. Check if the port is exposed:
```bash
docker port <container-id>
```

3. Try accessing via `http://127.0.0.1:5000` instead of `localhost`

## Customization

### Adding Questions
Edit `app.py` and add new questions to the `QUESTIONS` list:

```python
{
    "id": 21,
    "difficulty": "Hard",
    "question": "Your question here?",
    "type": "command",
    "answer": "correct-command",
    "hint": "Your hint here"
}
```

### Changing the Secret Key
Update the secret key in `app.py` for production:
```python
app.secret_key = 'your-production-secret-key'
```

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
