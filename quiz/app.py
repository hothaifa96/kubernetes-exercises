from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'application'

# 20 Docker and Kubernetes questions from easy to hard
QUESTIONS = [
    # Easy Questions (1-5)
    {
        "id": 1,
        "difficulty": "Easy",
        "question": "What command is used to list all running Docker containers?",
        "type": "command",
        "answer": "docker ps",
        "hint": "Think about 'process status' in Docker context"
    },
    {
        "id": 2,
        "difficulty": "Easy",
        "question": "What command builds a Docker image from a Dockerfile?",
        "type": "command",
        "answer": "docker build",
        "hint": "You need to 'build' something with Docker"
    },
    {
        "id": 3,
        "difficulty": "Easy",
        "question": "What command is used to list all Kubernetes pods in the current namespace?",
        "type": "command",
        "answer": "kubectl get pods",
        "hint": "Use kubectl to 'get' something"
    },
    {
        "id": 4,
        "difficulty": "Easy",
        "question": "What command stops a running Docker container?",
        "type": "command",
        "answer": "docker stop",
        "hint": "The opposite of starting a container"
    },
    {
        "id": 5,
        "difficulty": "Easy",
        "question": "What command removes a Docker image?",
        "type": "command",
        "answer": "docker rmi",
        "hint": "rmi stands for 'remove image'"
    },
    # Easy-Medium Questions (6-10)
    {
        "id": 6,
        "difficulty": "Easy-Medium",
        "question": "What command creates a Kubernetes deployment from a YAML file?",
        "type": "command",
        "answer": "kubectl apply -f",
        "hint": "You need to 'apply' a file"
    },
    {
        "id": 7,
        "difficulty": "Easy-Medium",
        "question": "What command shows detailed information about a Kubernetes pod?",
        "type": "command",
        "answer": "kubectl describe pod",
        "hint": "Use 'describe' to get more details"
    },
    {
        "id": 8,
        "difficulty": "Easy-Medium",
        "question": "What command pulls a Docker image from a registry?",
        "type": "command",
        "answer": "docker pull",
        "hint": "The opposite of pushing an image"
    },
    {
        "id": 9,
        "difficulty": "Easy-Medium",
        "question": "What command deletes a Kubernetes pod?",
        "type": "command",
        "answer": "kubectl delete pod",
        "hint": "Use 'delete' to remove resources"
    },
    {
        "id": 10,
        "difficulty": "Easy-Medium",
        "question": "What command shows logs from a Kubernetes pod?",
        "type": "command",
        "answer": "kubectl logs",
        "hint": "You want to see the 'logs'"
    },
    # Medium Questions (11-15)
    {
        "id": 11,
        "difficulty": "Medium",
        "question": "What command executes a command inside a running Docker container?",
        "type": "command",
        "answer": "docker exec",
        "hint": "You want to 'execute' something inside"
    },
    {
        "id": 12,
        "difficulty": "Medium",
        "question": "What command creates a Kubernetes namespace?",
        "type": "command",
        "answer": "kubectl create namespace",
        "hint": "Use 'create' to make a new namespace"
    },
    {
        "id": 13,
        "difficulty": "Medium",
        "question": "What command tags a Docker image before pushing to a registry?",
        "type": "command",
        "answer": "docker tag",
        "hint": "You need to add a 'tag' to the image"
    },
    {
        "id": 14,
        "difficulty": "Medium",
        "question": "What command shows resource usage of Kubernetes pods?",
        "type": "command",
        "answer": "kubectl top pods",
        "hint": "Use 'top' to see resource usage"
    },
    {
        "id": 15,
        "difficulty": "Medium",
        "question": "What command copies files from a Docker container to the host?",
        "type": "command",
        "answer": "docker cp",
        "hint": "cp stands for 'copy'"
    },
    # Medium-Hard Questions (16-18)
    {
        "id": 16,
        "difficulty": "Medium-Hard",
        "question": "What command scales a Kubernetes deployment to a specific number of replicas?",
        "type": "command",
        "answer": "kubectl scale deployment",
        "hint": "Use 'scale' to change replica count"
    },
    {
        "id": 17,
        "difficulty": "Medium-Hard",
        "question": "What command creates a Kubernetes pod from an image without a YAML file?",
        "type": "command",
        "answer": "kubectl run",
        "hint": "Use 'run' to create a pod directly"
    },
    {
        "id": 18,
        "difficulty": "Medium-Hard",
        "question": "What command shows all Kubernetes services in the cluster?",
        "type": "command",
        "answer": "kubectl get services",
        "hint": "Use 'get' to list services"
    },
    # Hard Questions (19-20)
    {
        "id": 19,
        "difficulty": "Hard",
        "question": "What command applies a Kubernetes configuration and waits for the resource to be ready?",
        "type": "command",
        "answer": "kubectl apply --wait",
        "hint": "Use 'apply' with a 'wait' flag"
    },
    {
        "id": 20,
        "difficulty": "Hard",
        "question": "What command port-forwards a local port to a Kubernetes pod?",
        "type": "command",
        "answer": "kubectl port-forward",
        "hint": "Use 'port-forward' to forward ports"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    session['current_question'] = 0
    session['score'] = 0
    session['answers'] = []
    return jsonify({
        'success': True,
        'total_questions': len(QUESTIONS)
    })

@app.route('/get_question', methods=['GET'])
def get_question():
    current = session.get('current_question', 0)
    
    if current >= len(QUESTIONS):
        return jsonify({
            'quiz_complete': True,
            'score': session.get('score', 0),
            'total': len(QUESTIONS),
            'answers': session.get('answers', [])
        })
    
    question = QUESTIONS[current]
    return jsonify({
        'question_number': current + 1,
        'total_questions': len(QUESTIONS),
        'difficulty': question['difficulty'],
        'question': question['question'],
        'type': question['type'],
        'hint': question['hint']
    })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    user_answer = data.get('answer', '').strip().lower()
    current = session.get('current_question', 0)
    
    if current >= len(QUESTIONS):
        return jsonify({'error': 'Quiz already completed'})
    
    question = QUESTIONS[current]
    correct_answer = question['answer'].strip().lower()
    
    # Check if answer is correct (allow for some flexibility)
    is_correct = user_answer == correct_answer or user_answer in correct_answer.split()
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    # Store answer
    answers = session.get('answers', [])
    answers.append({
        'question_number': current + 1,
        'question': question['question'],
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'is_correct': is_correct,
        'difficulty': question['difficulty']
    })
    session['answers'] = answers
    
    # Move to next question
    session['current_question'] = current + 1
    
    return jsonify({
        'success': True,
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'current_score': session.get('score', 0),
        'next_question': current + 1,
        'quiz_complete': current + 1 >= len(QUESTIONS)
    })

@app.route('/reset_quiz', methods=['POST'])
def reset_quiz():
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
