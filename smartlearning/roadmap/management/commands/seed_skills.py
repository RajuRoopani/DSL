from django.core.management.base import BaseCommand
from roadmap.models import Skill, Topic, Resource


SEED_DATA = {
    'DSA': {
        'name': 'DSA',
        'icon_emoji': '🧮',
        'category': 'computer_science',
        'description': 'Data Structures and Algorithms — the foundation of technical interviews and efficient software.',
        'topics': [
            {
                'title': 'Arrays & Strings',
                'difficulty': 'beginner', 'order': 1, 'estimated_hours': 3.0,
                'description': 'Master array manipulation, sliding window, and two-pointer patterns.',
                'resources': [
                    {'title': 'Arrays — CS50 Lecture', 'url': 'https://www.youtube.com/watch?v=ywg7cW0Txs4', 'resource_type': 'video', 'order': 1},
                    {'title': 'Array Problems — LeetCode Easy', 'url': 'https://leetcode.com/tag/array/', 'resource_type': 'exercise', 'order': 2, 'is_recommended': True},
                    {'title': 'Two Pointers Technique', 'url': 'https://www.geeksforgeeks.org/two-pointers-technique/', 'resource_type': 'article', 'order': 3},
                ],
            },
            {
                'title': 'Linked Lists',
                'difficulty': 'beginner', 'order': 2, 'estimated_hours': 2.5,
                'description': 'Singly and doubly linked lists, reversal, cycle detection.',
                'resources': [
                    {'title': 'Linked List — freeCodeCamp', 'url': 'https://www.youtube.com/watch?v=Hj_rA0dhr2I', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': "Floyd's Cycle Detection", 'url': 'https://www.geeksforgeeks.org/floyds-cycle-detection-algorithm/', 'resource_type': 'article', 'order': 2},
                    {'title': 'LeetCode Linked List Problems', 'url': 'https://leetcode.com/tag/linked-list/', 'resource_type': 'exercise', 'order': 3},
                ],
            },
            {
                'title': 'Stacks & Queues',
                'difficulty': 'beginner', 'order': 3, 'estimated_hours': 2.0,
                'description': 'LIFO and FIFO structures, monotonic stacks, BFS with queues.',
                'resources': [
                    {'title': 'Stack and Queue — GeeksForGeeks', 'url': 'https://www.geeksforgeeks.org/stack-data-structure/', 'resource_type': 'article', 'order': 1},
                    {'title': 'Stacks & Queues Problems', 'url': 'https://leetcode.com/tag/stack/', 'resource_type': 'exercise', 'order': 2, 'is_recommended': True},
                ],
            },
            {
                'title': 'Binary Search',
                'difficulty': 'intermediate', 'order': 4, 'estimated_hours': 2.0,
                'description': 'Classic binary search, search on answer, rotated arrays.',
                'resources': [
                    {'title': 'Binary Search — Visual Explained', 'url': 'https://www.youtube.com/watch?v=P3YID7liBug', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Binary Search Problems', 'url': 'https://leetcode.com/tag/binary-search/', 'resource_type': 'exercise', 'order': 2},
                ],
            },
            {
                'title': 'Trees & Binary Trees',
                'difficulty': 'intermediate', 'order': 5, 'estimated_hours': 4.0,
                'description': 'BST, tree traversals (DFS/BFS), lowest common ancestor.',
                'resources': [
                    {'title': 'Tree Traversals — Back to Back SWE', 'url': 'https://www.youtube.com/watch?v=86g8jAQug04', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Tree Problems — LeetCode', 'url': 'https://leetcode.com/tag/tree/', 'resource_type': 'exercise', 'order': 2},
                    {'title': 'Binary Search Tree — Visualgo', 'url': 'https://visualgo.net/en/bst', 'resource_type': 'interactive', 'order': 3},
                ],
            },
            {
                'title': 'Graphs',
                'difficulty': 'intermediate', 'order': 6, 'estimated_hours': 5.0,
                'description': 'BFS, DFS, topological sort, union-find, shortest paths.',
                'resources': [
                    {'title': 'Graph Algorithms — William Fiset', 'url': 'https://www.youtube.com/watch?v=09_LlHjoEiY', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Graph Problems — LeetCode', 'url': 'https://leetcode.com/tag/graph/', 'resource_type': 'exercise', 'order': 2},
                    {"title": "Dijkstra's Algorithm Explained", 'url': 'https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/', 'resource_type': 'article', 'order': 3},
                ],
            },
            {
                'title': 'Dynamic Programming',
                'difficulty': 'advanced', 'order': 7, 'estimated_hours': 6.0,
                'description': 'Memoization, tabulation, knapsack, longest subsequences.',
                'resources': [
                    {'title': 'DP for Beginners — freeCodeCamp', 'url': 'https://www.youtube.com/watch?v=oBt53YbR9Kk', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'DP Patterns — LeetCode Discuss', 'url': 'https://leetcode.com/discuss/general-discussion/458695/dynamic-programming-patterns', 'resource_type': 'article', 'order': 2},
                    {'title': 'DP Problems — LeetCode', 'url': 'https://leetcode.com/tag/dynamic-programming/', 'resource_type': 'exercise', 'order': 3},
                ],
            },
            {
                'title': 'Sorting & Searching',
                'difficulty': 'advanced', 'order': 8, 'estimated_hours': 3.0,
                'description': 'QuickSort, MergeSort, HeapSort, and their applications.',
                'resources': [
                    {'title': 'Sorting Algorithms Visualized', 'url': 'https://www.youtube.com/watch?v=kPRA0W1kECg', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Sorting Visualizer', 'url': 'https://visualgo.net/en/sorting', 'resource_type': 'interactive', 'order': 2},
                ],
            },
        ],
    },
    'Web Development': {
        'name': 'Web Development',
        'icon_emoji': '🌐',
        'category': 'web',
        'description': 'Full-stack web development from HTML basics to deployment.',
        'topics': [
            {
                'title': 'HTML & CSS Fundamentals',
                'difficulty': 'beginner', 'order': 1, 'estimated_hours': 3.0,
                'description': 'Semantic HTML, CSS box model, Flexbox, Grid.',
                'resources': [
                    {'title': 'HTML Full Course — freeCodeCamp', 'url': 'https://www.youtube.com/watch?v=pQN-pnXPaVg', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'CSS Flexbox — MDN', 'url': 'https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Flexbox', 'resource_type': 'documentation', 'order': 2},
                    {'title': 'CSS Grid Garden', 'url': 'https://cssgridgarden.com/', 'resource_type': 'interactive', 'order': 3},
                ],
            },
            {
                'title': 'JavaScript Fundamentals',
                'difficulty': 'beginner', 'order': 2, 'estimated_hours': 4.0,
                'description': 'Variables, functions, closures, promises, async/await.',
                'resources': [
                    {'title': 'JavaScript for Beginners — Traversy Media', 'url': 'https://www.youtube.com/watch?v=hdI2bqOjy3c', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'JavaScript.info', 'url': 'https://javascript.info/', 'resource_type': 'documentation', 'order': 2},
                    {'title': 'JS30 — 30 Day Challenge', 'url': 'https://javascript30.com/', 'resource_type': 'tutorial', 'order': 3},
                ],
            },
            {
                'title': 'DOM & Browser APIs',
                'difficulty': 'beginner', 'order': 3, 'estimated_hours': 2.0,
                'description': 'DOM manipulation, event listeners, fetch API.',
                'resources': [
                    {'title': 'DOM Crash Course — Traversy', 'url': 'https://www.youtube.com/watch?v=0ik6X4DJKCc', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Fetch API — MDN', 'url': 'https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API', 'resource_type': 'documentation', 'order': 2},
                ],
            },
            {
                'title': 'React Fundamentals',
                'difficulty': 'intermediate', 'order': 4, 'estimated_hours': 5.0,
                'description': 'Components, hooks (useState, useEffect), props, React Router.',
                'resources': [
                    {'title': 'React Full Course — freeCodeCamp', 'url': 'https://www.youtube.com/watch?v=bMknfKXIFA8', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Official React Docs', 'url': 'https://react.dev/learn', 'resource_type': 'documentation', 'order': 2},
                    {'title': 'Build a Todo App in React', 'url': 'https://www.freecodecamp.org/news/how-to-build-a-todo-app-with-react/', 'resource_type': 'tutorial', 'order': 3},
                ],
            },
            {
                'title': 'REST APIs & HTTP',
                'difficulty': 'intermediate', 'order': 5, 'estimated_hours': 3.0,
                'description': 'HTTP methods, status codes, REST design, consuming APIs.',
                'resources': [
                    {'title': 'REST API Crash Course — Traversy', 'url': 'https://www.youtube.com/watch?v=SLwpqD8n3d0', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'HTTP Status Codes — MDN', 'url': 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Status', 'resource_type': 'documentation', 'order': 2},
                ],
            },
            {
                'title': 'Node.js & Express',
                'difficulty': 'intermediate', 'order': 6, 'estimated_hours': 4.0,
                'description': 'Node runtime, Express routing, middleware, REST API server.',
                'resources': [
                    {'title': 'Node.js Crash Course — Traversy', 'url': 'https://www.youtube.com/watch?v=fBNz5xF-Kx4', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Build REST API with Node — freeCodeCamp', 'url': 'https://www.youtube.com/watch?v=l8WPWK9mS5M', 'resource_type': 'tutorial', 'order': 2},
                ],
            },
            {
                'title': 'Databases & SQL',
                'difficulty': 'advanced', 'order': 7, 'estimated_hours': 3.0,
                'description': 'SQL basics, joins, indexes, PostgreSQL with Node.',
                'resources': [
                    {'title': 'SQL Tutorial — Mode Analytics', 'url': 'https://mode.com/sql-tutorial/', 'resource_type': 'tutorial', 'order': 1, 'is_recommended': True},
                    {'title': 'SQLZoo Interactive', 'url': 'https://sqlzoo.net/', 'resource_type': 'interactive', 'order': 2},
                ],
            },
            {
                'title': 'Deployment & DevOps Basics',
                'difficulty': 'advanced', 'order': 8, 'estimated_hours': 2.5,
                'description': 'Git workflows, CI/CD, deploying to Vercel/Railway/Render.',
                'resources': [
                    {'title': 'Deploy Node App — freeCodeCamp', 'url': 'https://www.freecodecamp.org/news/how-to-deploy-nodejs-application-with-render/', 'resource_type': 'tutorial', 'order': 1, 'is_recommended': True},
                    {'title': 'GitHub Actions Crash Course', 'url': 'https://www.youtube.com/watch?v=eB0nUzAI7M8', 'resource_type': 'video', 'order': 2},
                ],
            },
        ],
    },
    'AI / Machine Learning': {
        'name': 'AI / Machine Learning',
        'icon_emoji': '🤖',
        'category': 'ai',
        'description': 'Machine learning fundamentals to applied deep learning and NLP.',
        'topics': [
            {
                'title': 'Python for ML',
                'difficulty': 'beginner', 'order': 1, 'estimated_hours': 3.0,
                'description': 'Python syntax, list comprehensions, file I/O, OOP for ML workflows.',
                'resources': [
                    {'title': 'Python for Data Science — freeCodeCamp', 'url': 'https://www.youtube.com/watch?v=LHBE6Q9XlzI', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Python Exercises — Kaggle', 'url': 'https://www.kaggle.com/learn/python', 'resource_type': 'interactive', 'order': 2},
                ],
            },
            {
                'title': 'NumPy & Pandas',
                'difficulty': 'beginner', 'order': 2, 'estimated_hours': 3.0,
                'description': 'Arrays, dataframes, data cleaning, groupby, merge.',
                'resources': [
                    {'title': 'NumPy & Pandas — Corey Schafer', 'url': 'https://www.youtube.com/watch?v=ZyhVh-qRZPA', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Pandas Tutorial — Kaggle', 'url': 'https://www.kaggle.com/learn/pandas', 'resource_type': 'interactive', 'order': 2},
                ],
            },
            {
                'title': 'Data Visualization',
                'difficulty': 'beginner', 'order': 3, 'estimated_hours': 2.0,
                'description': 'Matplotlib, Seaborn, plotting distributions and correlations.',
                'resources': [
                    {'title': 'Matplotlib Tutorial — Corey Schafer', 'url': 'https://www.youtube.com/watch?v=UO98lJQ3QGI', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Data Visualization — Kaggle', 'url': 'https://www.kaggle.com/learn/data-visualization', 'resource_type': 'interactive', 'order': 2},
                ],
            },
            {
                'title': 'Linear & Logistic Regression',
                'difficulty': 'intermediate', 'order': 4, 'estimated_hours': 3.0,
                'description': 'Loss functions, gradient descent, regularization, scikit-learn.',
                'resources': [
                    {'title': 'ML Crash Course — Google', 'url': 'https://developers.google.com/machine-learning/crash-course', 'resource_type': 'course', 'order': 1, 'is_recommended': True},
                    {'title': 'Intro to ML — Kaggle', 'url': 'https://www.kaggle.com/learn/intro-to-machine-learning', 'resource_type': 'interactive', 'order': 2},
                ],
            },
            {
                'title': 'Decision Trees & Ensembles',
                'difficulty': 'intermediate', 'order': 5, 'estimated_hours': 3.0,
                'description': 'Decision trees, random forests, gradient boosting (XGBoost).',
                'resources': [
                    {'title': 'StatQuest — Decision Trees', 'url': 'https://www.youtube.com/watch?v=7VeUPuFGJHk', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'Intermediate ML — Kaggle', 'url': 'https://www.kaggle.com/learn/intermediate-machine-learning', 'resource_type': 'interactive', 'order': 2},
                ],
            },
            {
                'title': 'Neural Networks',
                'difficulty': 'intermediate', 'order': 6, 'estimated_hours': 5.0,
                'description': 'Perceptrons, backpropagation, activation functions, PyTorch intro.',
                'resources': [
                    {'title': 'Neural Networks — 3Blue1Brown', 'url': 'https://www.youtube.com/watch?v=aircAruvnKk', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'PyTorch in 60 min', 'url': 'https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html', 'resource_type': 'tutorial', 'order': 2},
                ],
            },
            {
                'title': 'CNNs & Computer Vision',
                'difficulty': 'advanced', 'order': 7, 'estimated_hours': 5.0,
                'description': 'Convolutional layers, pooling, transfer learning with ResNet.',
                'resources': [
                    {'title': 'CNN Explained — Stanford CS231n', 'url': 'https://www.youtube.com/watch?v=vT1JzLTH4G4', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'fastai Practical Deep Learning', 'url': 'https://course.fast.ai/', 'resource_type': 'course', 'order': 2},
                ],
            },
            {
                'title': 'NLP Basics',
                'difficulty': 'advanced', 'order': 8, 'estimated_hours': 4.0,
                'description': 'Tokenization, word embeddings, transformers, HuggingFace.',
                'resources': [
                    {'title': 'NLP with Python — freeCodeCamp', 'url': 'https://www.youtube.com/watch?v=X2vAabgKiuM', 'resource_type': 'video', 'order': 1, 'is_recommended': True},
                    {'title': 'HuggingFace Course', 'url': 'https://huggingface.co/learn/nlp-course', 'resource_type': 'course', 'order': 2},
                ],
            },
        ],
    },
}


class Command(BaseCommand):
    help = 'Seed DSA, Web Development, and AI/ML skills with topics and resources'

    def handle(self, *args, **options):
        for skill_key, skill_data in SEED_DATA.items():
            skill, created = Skill.objects.update_or_create(
                name=skill_data['name'],
                defaults={
                    'icon_emoji': skill_data['icon_emoji'],
                    'category': skill_data['category'],
                    'description': skill_data['description'],
                    'popularity_score': 100.0,
                },
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} skill: {skill.icon_emoji} {skill.name}')

            for topic_data in skill_data['topics']:
                resources = topic_data.pop('resources', [])
                topic, _ = Topic.objects.update_or_create(
                    skill=skill,
                    title=topic_data['title'],
                    defaults={k: v for k, v in topic_data.items()},
                )
                for res_data in resources:
                    Resource.objects.update_or_create(
                        topic=topic,
                        title=res_data['title'],
                        defaults={k: v for k, v in res_data.items() if k != 'title'},
                    )
                self.stdout.write(f'  ✓ {topic.title} ({len(resources)} resources)')

        self.stdout.write(self.style.SUCCESS('\nSeed complete.'))
