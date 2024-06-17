import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

urls = {
    'REST': 'https://api.github.com/users/octocat/repos',
    'GraphQL': 'https://api.github.com/graphql'
}

token = 'TOKEN'

def measure_response(url, query=None):
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }
    start_time = time.time()
    
    if query:
        response = requests.post(url, json={'query': query}, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    
    end_time = time.time()
    response_time = end_time - start_time
    response_size = len(response.content)
    
    return response_time, response_size

results = {
    'API': [],
    'Complexity': [],
    'Response Time (s)': [],
    'Response Size (bytes)': []
}

graphql_queries = {
    'low': """
        {
          user(login: "octocat") {
            repositories(first: 10) {
              nodes {
                name
              }
            }
          }
        }
    """,
    'medium': """
        {
          user(login: "octocat") {
            repositories(first: 10) {
              nodes {
                name
                owner {
                  login
                }
              }
            }
          }
        }
    """,
    'high': """
        {
          user(login: "octocat") {
            repositories(first: 10) {
              nodes {
                name
                owner {
                  login
                }
                description
                stargazerCount
                forkCount
              }
            }
          }
        }
    """
}

measurements = {
    'low': 100,
    'medium': 150,
    'high': 250
}

for complexity, num_measurements in measurements.items():
    for _ in range(num_measurements):
        response_time, response_size = measure_response(urls['REST'])
        results['API'].append('REST')
        results['Complexity'].append(complexity)
        results['Response Time (s)'].append(response_time)
        results['Response Size (bytes)'].append(response_size)

for complexity, query in graphql_queries.items():
    num_measurements = measurements[complexity]
    for _ in range(num_measurements):
        response_time, response_size = measure_response(urls['GraphQL'], query)
        results['API'].append('GraphQL')
        results['Complexity'].append(complexity)
        results['Response Time (s)'].append(response_time)
        results['Response Size (bytes)'].append(response_size)

df = pd.DataFrame(results)
df.to_csv('experiment_results.csv', index=False)
print("Dados coletados e salvos em 'experiment_results.csv'")

df = pd.read_csv('experiment_results.csv')

print(df.describe())

for complexity in ['low', 'medium', 'high']:
    rest_data = df[(df['API'] == 'REST') & (df['Complexity'] == complexity)]
    graphql_data = df[(df['API'] == 'GraphQL') & (df['Complexity'] == complexity)]
    
    t_stat, p_value = stats.ttest_ind(rest_data['Response Time (s)'], graphql_data['Response Time (s)'])
    print(f"Complexidade: {complexity.capitalize()}")
    print(f"T-Statistic: {t_stat}, P-Value: {p_value}")
    print("")

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
df.boxplot(column='Response Time (s)', by=['API', 'Complexity'])
plt.title('Response Time Comparison')
plt.suptitle('')

plt.subplot(1, 2, 2)
df.boxplot(column='Response Size (bytes)', by=['API', 'Complexity'])
plt.title('Response Size Comparison')
plt.suptitle('')

plt.show()
