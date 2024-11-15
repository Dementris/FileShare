/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_APP_TITLE: string
    readonly VITE_BACKEND_URL: string
    readonly VITE_REFRESH_TOKEN_URL: string
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}