

export function getBackendHostname(): string {
    // returns
    // "http://localhost:5000" <- for development mode
    // or
    // "" <- for production mode
    return import.meta.env.VITE_API_URL
}

export function postJson(url: string, object: object) {
    return fetch(getBackendHostname() + url, {
        method: "POST", headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(object),
        credentials: "include",
    })
}

export function getJson(url: string): Response {
    return fetch(import.meta.env.VITE_API_URL + url, {
        credentials: "include",
    })
}


