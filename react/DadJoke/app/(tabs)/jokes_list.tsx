import { Text, View } from 'react-native';
import {useState, useEffect} from 'react';
import styles from '../../assets/my_styles';

type Joke = {
  id: number;
  text: string;
  contributer: string; 
  timestamp: string;
};

export default function JokesListScreen() {
  const [jokes, setJokes] = useState<Joke[]>([]);
  const fetchData = async () => {
    const response = await fetch(`https://cs-webapps.bu.edu/ksolter/dadjokes/api/jokes/`);
    const data = await response.json();
    setJokes(data.results);
  }

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <View style={styles.textContainer}>
      <Text style={styles.titleText}>Jokes List</Text>
      {jokes.map((joke) => (
        <View key={joke.id} style={styles.textContainer}>
          <Text style={styles.paragraphText}>{joke.text}</Text>
          <Text style={styles.paragraphText}>Contributed by: {joke.contributer}</Text>
          <Text style={styles.paragraphText}>Timestamp: {joke.timestamp}</Text>
        </View>
      ))}

    </View>
  );
}
