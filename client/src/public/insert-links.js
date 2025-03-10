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

  const preloadLinkEnergy = document.createElement("link")
  preloadLinkEnergy.rel = "preload"
  preloadLinkEnergy.href = `${apiUrl}/energy`
  preloadLinkEnergy.as = "fetch"
  preloadLinkEnergy.crossOrigin = "anonymous"
  head.appendChild(preloadLinkEnergy)

  const preloadLinkPrice = document.createElement("link")
  preloadLinkPrice.rel = "preload"
  preloadLinkPrice.href = `${apiUrl}/price`
  preloadLinkPrice.as = "fetch"
  preloadLinkPrice.crossOrigin = "anonymous"
  head.appendChild(preloadLinkPrice)
})()
