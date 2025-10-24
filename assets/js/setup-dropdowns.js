let triggerDropdownCurry = function(btn, content) {
  return function(e) {
    if (content.classList.contains("hidden")) {
      content.classList.remove("hidden")
      btn.innerText = "v"
    } else {
      btn.innerText = ">"
      content.classList.add("hidden")
    }
  }
}
/**
 * @param {HTMLElement} el The element to set up with a drop down
 * @param {HTMLButtonElement} dropDownBtn The drop down button to use
 */
let setupDropdown = function(el, dropDownBtn) {
  let content = null
  let children = el.children
  for (let i = 0; i < children.length; i++) {
    if (children[i].classList.contains("dropdown-content")) {
      content = children[i]
      break
    }
  }
  if (content === null) {
    return;
  }
  dropDownBtn.addEventListener("click", triggerDropdownCurry(dropDownBtn, content))
}
let dropDowns = document.querySelectorAll("dropdown-container")
for (let i = 0; i < dropDowns.length; i++) {
  let dropDown = dropDowns[i]
  if (dropDown.id == null) {
    dropDown.id = "dropdown-" + i
  }
  let btn = document.querySelector(`${dropDowns[i].id} dropdown`)
  setupDropdown(dropDown, btn)
}
