
    // Service worker para controle externo
    
    // Escuta mensagens do native host Python
    chrome.runtime.onMessageExternal.addListener(
        function(request, sender, sendResponse) {
            console.log("Comando recebido:", request);
            
            if (request.action === "navigate") {
                chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                    chrome.tabs.update(tabs[0].id, {url: request.url});
                    sendResponse({success: true, tabId: tabs[0].id});
                });
                return true; // Mantém canal aberto para resposta assíncrona
            }
            
            if (request.action === "inject") {
                chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                    chrome.scripting.executeScript({
                        target: {tabId: tabs[0].id},
                        func: () => {
                            // Remove webdriver
                            delete navigator.__proto__.webdriver;
                            // Adiciona propriedades Chrome
                            if (!window.chrome) {
                                window.chrome = {runtime: {}, loadTimes: function() {}};
                            }
                        }
                    });
                    sendResponse({success: true});
                });
                return true;
            }
        }
    );
    
    // Injeta anti-detecção em todas as páginas
    chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
        if (changeInfo.status === 'complete') {
            chrome.scripting.executeScript({
                target: {tabId: tabId},
                func: () => {
                    // Script anti-detecção
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    
                    // Chrome runtime
                    if (!window.chrome || !window.chrome.runtime) {
                        window.chrome = window.chrome || {};
                        window.chrome.runtime = {};
                    }
                    
                    // Plugins
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5].map((i) => ({
                            name: `Plugin ${i}`,
                            filename: `plugin${i}.dll`,
                            description: `Description ${i}`
                        }))
                    });
                }
            });
        }
    });
    