<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Nyay AI - AI Lok Adalat</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 20px;
      background-color: #f8f9fa;
      color: #212529;
    }
    h2 {
      color: #123366;
    }
    label, select, textarea, button {
      display: block;
      margin-bottom: 12px;
      width: 100%;
    }
    select, textarea {
      padding: 10px;
      font-size: 1rem;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
    button {
      padding: 10px;
      background-color: #bfa14b;
      color: #fff;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-weight: bold;
    }
    button:hover {
      background-color: #a38736;
    }
    #finalAgreement, #clarifyingQuestions {
      margin-top: 20px;
      padding: 16px;
      background-color: #ffffff;
      border: 1px solid #ccc;
      border-radius: 8px;
      display: none;
    }
  </style>
</head>
<body>
  <h2>🪙 AI Lok Adalat - Instant Dispute Resolution (Beta)</h2>

  <form id="mediationForm">
    <label for="disputeType">Choose Dispute Type:</label>
    <select id="disputeType" name="dispute_type" required>
      <option value="rent">🏠 Rent Issue</option>
      <option value="property">🏡 Property Dispute</option>
      <option value="noise">🔊 Neighbor Noise</option>
    </select>

    <div id="clarifyingQuestions"></div>

    <label for="userResponse">💬 Your response to the above questions:</label>
    <textarea id="userResponse" name="user_input" rows="4" placeholder="Write your answers here..." required></textarea>

    <button type="submit" id="submitAnswers">Submit Answers</button>
  </form>

  <div id="finalAgreement"></div>

  <script>
    const clarifyingMap = {
      rent: `1. What was the agreed rent and payment frequency?\n2. Has any rent been paid?\n3. Were there discussions about delay?\n4. Any other problems like damage or misbehavior?`,
      property: `1. Who owns the property legally?\n2. What documents are involved?\n3. Any ongoing legal case?\n4. What resolution are you expecting?`,
      noise: `1. What kind of noise disturbance?\n2. How frequent is the problem?\n3. Have you talked to the neighbor?\n4. Any police complaint or society involvement?`
    };

    const disputeTypeSelect = document.getElementById("disputeType");
    const clarifyingQuestionsDiv = document.getElementById("clarifyingQuestions");
    const finalAgreementDiv = document.getElementById("finalAgreement");
    const responseBox = document.getElementById("userResponse");
    const submitBtn = document.getElementById("submitAnswers");

    disputeTypeSelect.addEventListener("change", () => {
      const selected = disputeTypeSelect.value;
      clarifyingQuestionsDiv.style.display = "block";
      clarifyingQuestionsDiv.innerHTML = `<strong>📋 Questions:</strong><br><br>${clarifyingMap[selected].replace(/\n/g, '<br>')}`;
    });

    document.getElementById("mediationForm").addEventListener("submit", async function (e) {
      e.preventDefault();

      const disputeType = disputeTypeSelect.value;
      const userInput = responseBox.value;

      // Fake server response simulation
      const solution = `🤝 Based on your response for '${disputeType}' dispute, the suggested settlement is:\nBoth parties agree to resolve the issue amicably within 7 days. Rent payments must be cleared, or further legal mediation may be pursued.`;

      // Hide inputs and show result
      clarifyingQuestionsDiv.style.display = "none";
      responseBox.style.display = "none";
      submitBtn.style.display = "none";

      finalAgreementDiv.innerHTML = `<strong>📄 Suggested Settlement:</strong><br><br>${solution.replace(/\n/g, '<br>')}`;
      finalAgreementDiv.style.display = "block";
    });

    // Initialize with default questions
    disputeTypeSelect.dispatchEvent(new Event("change"));
  </script>
</body>
</html>
