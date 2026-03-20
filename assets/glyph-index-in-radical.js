// Close the popover when clicking any link inside #index
document.querySelector('#index')?.addEventListener('click', (e) => {
    if (e.target.closest('a')) {
        document.querySelector('#index').hidePopover();
    }
});
