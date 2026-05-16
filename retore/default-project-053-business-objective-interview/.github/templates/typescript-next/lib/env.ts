import { z } from "zod"

const envSchema = z.object({
    NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
    NEXT_PUBLIC_APP_URL: z.string().url().default("http://localhost:3000"),
    // Adicionar variáveis obrigatórias do projeto aqui:
    // DATABASE_URL: z.string().url(),
})

// Lança erro imediatamente se variáveis obrigatórias estão ausentes (fail fast)
export const env = envSchema.parse(process.env)
