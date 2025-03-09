;(function () {
  let apiUrl
  try {
    apiUrl = new URL("__API_URL__")
  } catch {
    apiUrl = new URL("http://localhost:8000/data")
  }

  const head = document.head

  const preconnectLink = document.createElement("link")
  preconnectLink.rel = "preconnect"
  preconnectLink.href = apiUrl.origin
  preconnectLink.crossOrigin = "anonymous"
  head.appendChild(preconnectLink)

  const dnsPrefetchLink = document.createElement("link")
  dnsPrefetchLink.rel = "dns-prefetch"
  dnsPrefetchLink.href = apiUrl.origin
  head.appendChild(dnsPrefetchLink)

  const preloadLink = document.createElement("link")
  preloadLink.rel = "preload"
  preloadLink.href = apiUrl
  preloadLink.as = "fetch"
  preloadLink.crossOrigin = "anonymous"
  head.appendChild(preloadLink)
})()
