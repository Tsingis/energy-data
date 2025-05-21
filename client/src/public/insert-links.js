;(function () {
  try {
    const apiBaseUrl = new URL("__API_URL__")
    const head = document.head

    const preconnectLink = document.createElement("link")
    preconnectLink.rel = "preconnect"
    preconnectLink.href = apiBaseUrl.origin
    preconnectLink.crossOrigin = "anonymous"
    head.appendChild(preconnectLink)

    const dnsPrefetchLink = document.createElement("link")
    dnsPrefetchLink.rel = "dns-prefetch"
    dnsPrefetchLink.href = apiBaseUrl.origin
    head.appendChild(dnsPrefetchLink)

    const preloadLinkEnergy = document.createElement("link")
    preloadLinkEnergy.rel = "preload"
    preloadLinkEnergy.href = `${apiBaseUrl}api/energy`
    preloadLinkEnergy.as = "fetch"
    preloadLinkEnergy.crossOrigin = "anonymous"
    head.appendChild(preloadLinkEnergy)

    const preloadLinkPrice = document.createElement("link")
    preloadLinkPrice.rel = "preload"
    preloadLinkPrice.href = `${apiBaseUrl}api/price`
    preloadLinkPrice.as = "fetch"
    preloadLinkPrice.crossOrigin = "anonymous"
    head.appendChild(preloadLinkPrice)
  } catch {
    console.error("Error creating preconnects")
  }
})()
