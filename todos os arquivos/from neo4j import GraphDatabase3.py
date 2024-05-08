from neo4j import GraphDatabase
import csv

class Neo4jConnection:
    
    def __init__(self, uri, user, password):
        # Certifique-se de usar o esquema de URI correto para conexões seguras com o Neo4j Aura
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()

    def create_indexes(self):
        with self.driver.session() as session:
            # Cria um índice para a propriedade PLAYER do nó Player
            session.run("CREATE INDEX IF NOT EXISTS FOR (p:Player) ON (p.PLAYER)")

    def import_players(self, csv_file):
        with self.driver.session() as session:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Cria o nó Player com as propriedades do arquivo CSV
                    session.run(
                        "CREATE (p:Player {PlayerID: $PlayerID, PLAYER: $PLAYER, COUNTRY: $COUNTRY, TEAM: $TEAM, ACS: $ACS, KD: $KD})",
                        parameters={
                            'PlayerID': int(row['PlayerID']), 
                            'PLAYER': row['PLAYER'], 
                            'COUNTRY': row['COUNTRY'], 
                            'TEAM': row['TEAM'], 
                            'ACS': float(row['ACS']), 
                            'KD': float(row['KD'])
                        }
                    )

if __name__ == "__main__":
    # Substitua pela sua URL de conexão do Neo4j Aura
    neo4j_url = "neo4j+ssc://ee9c4b83.databases.neo4j.io"
    neo4j_username = "neo4j"
    neo4j_password = "4hEAOFQAinB6I7iVx00mSZtlFCVXST6ez4ie3MPYNtA"
    csv_file = 'Arquivo CSV/Arquivo_transicao/tbl_players.csv'
    
    conn = Neo4jConnection(neo4j_url, neo4j_username, neo4j_password)
    try:
        conn.create_indexes()
        conn.import_players(csv_file)
    finally:
        conn.close()
