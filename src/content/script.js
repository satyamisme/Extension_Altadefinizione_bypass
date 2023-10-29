(async () => {
    const src = chrome.runtime.getURL('src/content/main.js')
    const contentScript = await import(src)
})()
  