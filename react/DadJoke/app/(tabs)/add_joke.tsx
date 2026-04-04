import { useState } from 'react';
import { Alert, Pressable, Text, TextInput, View } from 'react-native';
import styles from '../../assets/my_styles';

export default function AddJokeScreen() {
	const [jokeText, setJokeText] = useState('');
	const [contributorName, setContributorName] = useState('');

	const submitJoke = async () => {
		const text = jokeText.trim();
		const contributer = contributorName.trim();

		if (!text || !contributer) {
			Alert.alert('Missing fields', 'Please enter both a joke and contributor name.');
			return;
		}

		try {
			let response = await fetch('https://cs-webapps.bu.edu/ksolter/dadjokes/api/jokes/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ text, contributer }),
			});

			if (!response.ok) {
				response = await fetch('https://cs-webapps.bu.edu/ksolter/dadjokes/api/jokes/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ text, contributor: contributer }),
				});
			}

			if (response.ok) {
				setJokeText('');
				setContributorName('');
				Alert.alert('Success', 'Joke submitted.');
			} else {
				Alert.alert('Submit failed', `Server returned ${response.status}.`);
			}
		} catch {
			console.log('Network error', 'Could not reach the API endpoint.');
		}
	};

	return (
		<View style={styles.mediumContainer}>
			<Text style={styles.titleText}>Add Joke</Text>
			<View style={styles.inputboxcontainer}>
				<TextInput
					style={styles.inputbox}
					placeholder="Enter joke text"
					placeholderTextColor="black"
					value={jokeText}
					onChangeText={setJokeText}
				/>
			</View>

			<View style={styles.inputboxcontainer}>
				<TextInput
					style={styles.inputbox}
					placeholder="Enter contributor name"
					placeholderTextColor="black"
					value={contributorName}
					onChangeText={setContributorName}
				/>
			</View>

			<Pressable
				onPress={submitJoke}
				style={({ pressed }) => [styles.submitButton, pressed && styles.submitButtonPressed]}
			>
				<Text style={styles.submitButtonText}>Submit Joke</Text>
			</Pressable>
		</View>
	);
}
