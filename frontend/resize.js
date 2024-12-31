const resizer = document.getElementById('resizer');
const leftSection = document.getElementById('formSection');
const rightSection = document.getElementById('chatSection');
let isResizing = false;

// To store the initial positions of mouse when resizing starts
let startX = 0;
let startLeftWidth = 0;

// Mouse down event to start resizing
resizer.addEventListener('mousedown', (event) => {
    isResizing = true;
    startX = event.clientX; // Initial mouse position
    startLeftWidth = leftSection.offsetWidth; // Current width of left section

    // Add mousemove and mouseup listeners
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', () => {
        isResizing = false;
        document.removeEventListener('mousemove', handleMouseMove);
    });
});

// Mouse move event to resize sections and move the resizer
function handleMouseMove(event) {
    if (!isResizing) return;

    // Calculate the new width based on mouse movement
    const deltaX = event.clientX - startX;
    let newLeftWidth = ((startLeftWidth + deltaX) / window.innerWidth) * 100;

    // Ensure that the width stays within a reasonable range (20% to 80%)
    newLeftWidth = Math.max(20, Math.min(newLeftWidth, 80));

    // Update the width of the left and right sections
    leftSection.style.width = `${newLeftWidth}%`;
    rightSection.style.width = `${100 - newLeftWidth}%`;

    // Move the resizer along with the mouse
    const newResizerPosition = newLeftWidth + '%'; // Move the resizer to match the left section's width
    resizer.style.left = newResizerPosition;
}
