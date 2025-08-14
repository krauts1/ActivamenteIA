export type Source = {
    rid: number
    score: number
    text: string
    meta?: Record<string, any>
  }
  
  export type QueryResponse = {
    answer: string
    sources: Source[]
    sql: Array<Record<string, any>> | null
  }
  
  export type Health = {
    status: string
    index_size: number
  }
  