(function(){
    console.log(`reminiscence-bookmarklet starts`);
    /*
    window.open(
        `{{target_url}}?directory=AddToReminiscence&url=${encodeURIComponent(document.location.href)}`
    );
    */
    window.location.href = `{{target_url}}?directory=AddToReminiscence&url=${encodeURIComponent(document.location.href)}`;
    console.log(`reminiscence-bookmarklet ends`);
})();
