export interface AggregateArticle {
    title: string
    imageUrl: string
    sources: {
        name: string
        url: string
        citation: string
    }[]
    url: string
    latestUpdateDateTime: Date
    updateHistory: {
        dateTime: Date
        description: string
    }[]
    description: string
    tags: string[]
  }
export class ApiClient {
    private baseUrl: string
  
    constructor() {
      this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:10000'
    }
  
    private async request<T>(path: string, options?: RequestInit): Promise<T> {
      const url = `${this.baseUrl}${path}`
  
      const res = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
        },
        ...options,
      })
  
      if (!res.ok) {
        throw new Error(`API request failed: ${res.status} ${res.statusText}`)
      }
  
      return (await res.json()) as T
    }
  
    async getNews(): Promise<AggregateArticle[]> {
      try {
        const response = await fetch(`${this.baseUrl}/api/news`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.articles || [];
      } catch (error) {
        console.error('Error fetching news:', error);
        throw error;
      }
    }

    async triggerAggregation(): Promise<unknown> {
      try {
        const response = await fetch(`${this.baseUrl}/api/aggregate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
      } catch (error) {
        console.error('Error triggering aggregation:', error);
        throw error;
      }
    }
}
  