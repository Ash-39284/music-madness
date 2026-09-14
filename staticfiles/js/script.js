function toggleReply(id) {
    const el = document.getElementById(id);
    el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

// Required for Jest testing
if (typeof module !== 'undefined') {
    module.exports = { toggleReply };
}