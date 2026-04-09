document.getElementById('feedbackForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    const responseMsg = document.getElementById('responseMessage');

    // Get form data
    const formData = new FormData(form);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        rating: parseInt(formData.get('rating')),
        experience: formData.get('experience')
    };

    // UI state: Loading
    submitBtn.disabled = true;
    btnText.textContent = 'Sending...';
    loader.classList.remove('hidden');
    responseMsg.classList.add('hidden');

    try {
        const response = await fetch('/submit-feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (response.ok) {
            responseMsg.textContent = '✅ Thank you! Your feedback has been received.';
            responseMsg.className = 'message success';
            form.reset();
        } else {
            throw new Error(result.detail || 'Something went wrong');
        }
    } catch (error) {
        responseMsg.textContent = `❌ Error: ${error.message}`;
        responseMsg.className = 'message error';
    } finally {
        submitBtn.disabled = false;
        btnText.textContent = 'Send Feedback';
        loader.classList.add('hidden');
        responseMsg.classList.remove('hidden');
    }
});
