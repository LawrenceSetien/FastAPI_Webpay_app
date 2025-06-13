document.addEventListener('DOMContentLoaded', () => {
    const loadingStatus = document.getElementById('loadingStatus');
    const paymentResult = document.getElementById('paymentResult');
    const errorResult = document.getElementById('errorResult');
    const resultContent = document.getElementById('resultContent');
    const errorMessage = document.getElementById('errorMessage');

    // Get the token from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token_ws');

    // Button event listeners
    document.getElementById('backButton')?.addEventListener('click', () => {
        window.location.href = '/';
    });

    document.getElementById('newPaymentButton')?.addEventListener('click', () => {
        window.location.href = '/';
    });

    document.getElementById('retryButton')?.addEventListener('click', () => {
        window.location.href = '/';
    });

    document.getElementById('homeButton')?.addEventListener('click', () => {
        window.location.href = '/';
    });

    // Check if we have a token
    if (!token) {
        showError('No payment token found. Please try making a payment again.');
        return;
    }

    // Confirm the payment
    confirmPayment(token);

    async function confirmPayment(token) {
        try {
            const response = await fetch(`/payments/confirm?token=${encodeURIComponent(token)}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.ok) {
                showSuccess(data);
            } else {
                throw new Error(data.detail || 'Payment confirmation failed');
            }
        } catch (error) {
            console.error('Payment confirmation error:', error);
            showError(`Error confirming payment: ${error.message}`);
        }
    }

    function showSuccess(data) {
        loadingStatus.classList.add('hidden');
        paymentResult.classList.remove('hidden');
        
        const statusIcon = data.status === 'AUTHORIZED' ? '✅' : '⚠️';
        const statusText = data.status === 'AUTHORIZED' ? 'Payment Successful!' : 'Payment Status: ' + data.status;
        
        resultContent.innerHTML = `
            <div class="status-success">
                <h2>${statusIcon} ${statusText}</h2>
                <div class="payment-details">
                    <div class="detail-row">
                        <span class="label">Amount:</span>
                        <span class="value">$${data.amount.toLocaleString()} CLP</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Order ID:</span>
                        <span class="value">${data.buy_order}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Session ID:</span>
                        <span class="value">${data.session_id}</span>
                    </div>
                    ${data.card_number ? `
                    <div class="detail-row">
                        <span class="label">Card Number:</span>
                        <span class="value">**** **** **** ${data.card_number}</span>
                    </div>
                    ` : ''}
                    ${data.transaction_date ? `
                    <div class="detail-row">
                        <span class="label">Transaction Date:</span>
                        <span class="value">${new Date(data.transaction_date).toLocaleString()}</span>
                    </div>
                    ` : ''}
                    ${data.authorization_code ? `
                    <div class="detail-row">
                        <span class="label">Authorization Code:</span>
                        <span class="value">${data.authorization_code}</span>
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    function showError(message) {
        loadingStatus.classList.add('hidden');
        errorResult.classList.remove('hidden');
        errorMessage.textContent = message;
    }
}); 