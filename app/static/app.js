document.addEventListener('DOMContentLoaded', () => {
    const payButton = document.getElementById('payButton');
    const amountInput = document.getElementById('amount');
    const buyOrderInput = document.getElementById('buyOrder');
    const sessionIdInput = document.getElementById('sessionId');
    const paymentStatus = document.getElementById('paymentStatus');
    const statusContent = document.getElementById('statusContent');

    // Generate a random order ID if not provided
    if (!buyOrderInput.value || buyOrderInput.value === 'ORDER-123') {
        buyOrderInput.value = `ORDER-${Math.random().toString(36).substr(2, 9)}`;
    }
    // Generate a random session ID if not provided
    if (!sessionIdInput.value || sessionIdInput.value === 'SESSION-123') {
        sessionIdInput.value = `SESSION-${Math.random().toString(36).substr(2, 9)}`;
    }

    payButton.addEventListener('click', async () => {
        try {
            payButton.disabled = true;
            payButton.textContent = 'Processing...';

            const paymentData = {
                amount: parseFloat(amountInput.value),
                buy_order: buyOrderInput.value,
                session_id: sessionIdInput.value,
                return_url: `${window.location.origin}/payment-result`
            };

            const response = await fetch('/payments/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(paymentData)
            });

            const data = await response.json();

            if (response.ok) {
                // Redirect to Transbank payment page
                const paymentUrl = `${data.url}?token_ws=${data.token}`;
                window.location.href = paymentUrl;
            } else {
                throw new Error(data.detail || 'Payment creation failed');
            }
        } catch (error) {
            showStatus('error', `Error: ${error.message}`);
            payButton.disabled = false;
            payButton.textContent = 'Pay Now';
        }
    });

    function showStatus(type, content) {
        paymentStatus.classList.remove('hidden');
        statusContent.innerHTML = content;
        statusContent.className = `status-${type}`;
    }
});