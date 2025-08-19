let doPermalinks = function() {
    let els = document.querySelectorAll(".page-content > h1,.page-content > h2, .page-content > h3, .page-content > h4, .page-content > h5, .page-content > h6");
    for (let i = 0; i < els.length; i++) {
        if (els[i].id == null) {
            continue;
        }
        let elBase = document.createElement("a");
        elBase.className = "permalink";
        elBase.href = location.protocol + '//' + location.host + location.pathname + '#' + els[i].id
        elBase.innerText = "#"
        els[i].appendChild(elBase);
    }
};
if (document.readyState == 'loading') {
    document.addEventListener("DOMContentLoaded", doPermalinks);
} else {
    doPermalinks();
}
