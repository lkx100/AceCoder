document.addEventListener("DOMContentLoaded", function() {
    // Find all <pre> elements
    document.querySelectorAll('pre').forEach(function(preBlock) {
        // Create a button
        const copyButton = document.createElement('button');
        copyButton.innerText = 'Copy';
        copyButton.classList.add('copy-button');
        
        // Insert the button before the <pre> block
        preBlock.parentNode.insertBefore(copyButton, preBlock);

        // Add click event listener to copy the code
        copyButton.addEventListener('click', function() {
            const code = preBlock.querySelector('code').innerText;
            navigator.clipboard.writeText(code).then(function() {
                copyButton.innerText = 'Copied!';
                setTimeout(() => copyButton.innerText = 'Copy', 2000); // Reset button after 2 seconds
            }, function(err) {
                console.error('Could not copy text: ', err);
            });
        });
    });
});

