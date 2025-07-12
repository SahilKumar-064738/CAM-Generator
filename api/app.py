from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Fixed Set II sentences (PO1 to PSO2)
set_ii = [
    "Engineering Knowledge Apply the knowledge of mathematics, science, engineering fundamentals, and an engineering specialization to the solution of complex engineering problems.",  # PO1
    "Problem Analysis Identify, formulate, review research literature, and analyze complex engineering problems using first principles of mathematics, natural sciences, and engineering sciences.",  # PO2
    "Design/Development of Solutions Design solutions for complex engineering problems and design system components or processes that meet specified needs with appropriate consideration for public health, safety, cultural, societal, and environmental aspects.",  # PO3
    "Conduct Investigations of Complex Problems Use research-based knowledge and methods, including design of experiments, analysis and interpretation of data, and synthesis of information to provide valid conclusions.",  # PO4
    "Modern Tool Usage Create, select, and apply appropriate techniques, resources, and modern engineering and IT tools for engineering activities, with an understanding of limitations.",  # PO5
    "The Engineer and Society Apply reasoning informed by contextual knowledge to assess societal, health, safety, legal, and cultural issues relevant to professional engineering practice.",  # PO6
    "Environment and Sustainability Understand the impact of professional engineering solutions in societal and environmental contexts, and demonstrate knowledge of sustainable development.",  # PO7
    "Ethics Apply ethical principles and commit to professional ethics and responsibilities and norms of engineering practice.",  # PO8
    "Individual and Team Work Function effectively as an individual, and as a member or leader in diverse teams and in multidisciplinary settings.",  # PO9
    "Communication Communicate effectively on complex engineering activities with the engineering community and with society at large, including writing effective reports, making presentations, and giving and receiving clear instructions.",  # PO10
    "Project Management and Finance Demonstrate knowledge and understanding of engineering and management principles and apply these to one’s own work, as a member or leader in a team, to manage projects.",  # PO11
    "Life-long Learning Recognize the need for, and have the preparation and ability to engage in independent and lifelong learning.",  # PO12
    "Software Development Skills Apply the knowledge of computer science to develop algorithms and software solutions for real-world problems.",  # PSO1
    "System Design and Application Apply modern tools and techniques to design and implement efficient computer-based systems in multidisciplinary domains."  # PSO2
]

@app.route('/rate', methods=['POST'])
def rate_sentences():
    data = request.json
    set_i = data.get('set_i')

    if not set_i or not isinstance(set_i, list):
        return jsonify({'error': 'Invalid or missing "set_i" list'}), 400

    emb_i = model.encode(set_i, convert_to_tensor=True)
    emb_ii = model.encode(set_ii, convert_to_tensor=True)

    result = []
    for sent2, emb2 in zip(set_ii, emb_ii):
        row = {'SET_II_Sentence': sent2}
        print(f"\nComparing for: {sent2}")  # Debug: shows the PO/PSO sentence

        for i, emb1 in enumerate(emb_i):
            sim = util.cos_sim(emb2, emb1).item()
            print(f"Similarity with SET_I_{i+1}: {sim:.4f}")  # Debug similarity

            if sim > 0.25:
                rating = 3
            elif sim > 0.2:
                rating = 2
            elif sim > 0.1:
                rating = 1
            else:
                rating = 0

            print(f"Assigned rating: {rating}")  # Debug rating
            row[f"SET_I_{i+1}"] = rating  # Properly assign rating per SET_I

        result.append(row)  # Append after full inner loop

    return jsonify(result)

if __name__ == '__main__':
    app.run()
