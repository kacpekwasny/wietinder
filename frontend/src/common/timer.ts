
export async function timer(ms: number) {
    return new Promise(res => setTimeout(res, ms))
}

