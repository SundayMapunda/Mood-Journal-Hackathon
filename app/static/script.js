document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-messages li');
    
    flashMessages.forEach(message => {
        // Add slide-in animation class
        message.style.animation = 'slideIn 0.5s ease';
        
        // Set timeout to remove message after 5 seconds with slide-out
        setTimeout(() => {
            message.style.animation = 'slideOut 0.5s ease';
            message.style.opacity = '0';
            
            // Remove after animation completes
            setTimeout(() => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 500); // Match animation duration
        }, 3000); // 5 seconds display time
    });
});
