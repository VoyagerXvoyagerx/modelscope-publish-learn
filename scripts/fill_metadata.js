/**
 * Fill ModelScope article metadata form fields programmatically.
 * Run this via evaluate() in the browser on /learn/editor/{id} page.
 *
 * @param {Object} metadata
 * @param {string} metadata.title
 * @param {string} metadata.description
 * @param {string} metadata.subject - e.g. "数据集"
 * @param {string} metadata.domain - e.g. "人工智能"
 */
function fillModelScopeMetadata(metadata) {
  const results = [];

  // 1. Fill Title
  const titleInput = document.querySelector("input#Title");
  if (titleInput) {
    titleInput.focus();
    titleInput.value = metadata.title || "";
    titleInput.dispatchEvent(new Event("input", { bubbles: true }));
    results.push("title: filled");
  } else {
    results.push("title: not found");
  }

  // 2. Fill Description (use native setter for React-controlled textarea)
  const descTa = document.querySelector("textarea#Description");
  if (descTa) {
    descTa.focus();
    const text = metadata.description || "";
    const nativeSetter = Object.getOwnPropertyDescriptor(
      window.HTMLTextAreaElement.prototype,
      "value"
    ).set;
    nativeSetter.call(descTa, text);
    descTa.dispatchEvent(new Event("input", { bubbles: true }));
    results.push("description: filled");
  } else {
    results.push("description: not found");
  }

  // 3. Select Subject
  if (metadata.subject) {
    const subjInput = document.querySelector("input#Subjects");
    if (subjInput) {
      subjInput.focus();
      subjInput.value = metadata.subject;
      subjInput.dispatchEvent(new Event("input", { bubbles: true }));
      // Try to click the dropdown option
      setTimeout(() => {
        const options = document.querySelectorAll(
          ".antd5-select-dropdown .antd5-select-item"
        );
        for (const opt of options) {
          if (opt.innerText.trim() === metadata.subject) {
            opt.click();
            break;
          }
        }
      }, 300);
      results.push("subject: filled");
    } else {
      results.push("subject: not found");
    }
  }

  // 4. Select Domain
  if (metadata.domain) {
    const domainInput = document.querySelector("input#Domains");
    if (domainInput) {
      domainInput.focus();
      domainInput.value = metadata.domain;
      domainInput.dispatchEvent(new Event("input", { bubbles: true }));
      setTimeout(() => {
        const options = document.querySelectorAll(
          ".antd5-select-dropdown .antd5-select-item"
        );
        for (const opt of options) {
          if (opt.innerText.trim() === metadata.domain) {
            opt.click();
            break;
          }
        }
      }, 300);
      results.push("domain: filled");
    } else {
      results.push("domain: not found");
    }
  }

  // 5. Select default cover image (blue)
  const coverImg = document.querySelector('img[src*="learn_blue.png"]');
  if (coverImg) {
    coverImg.click();
    results.push("cover: selected");
  } else {
    results.push("cover: not found");
  }

  return JSON.stringify(results);
}

// If run directly with metadata argument
if (typeof window !== "undefined" && window.__modelscope_metadata__) {
  fillModelScopeMetadata(window.__modelscope_metadata__);
}
