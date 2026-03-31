// react/MyApps/app/(tabs)/about.tsx 
// Author: Kai Solter
// This is a static screen which displays images and text
import { Text, View, Image } from 'react-native';
import styles from '@/assets/my_styles';
const d1 = require('@/assets/images/denjiorigin1.png');
const d2 = require('@/assets/images/denjiorigin2.png');

export default function AboutScreen() {
	return (
		<View>
			<Text style={styles.titleText}>About CSM!</Text>

            <Image source={d1} style={styles.image} />
            <Image source={d2} style={styles.wideImage} />
            <Text style={styles.subTitleText}>This is denji's (the main character) origin. 
                When he was about to die he made a contract with a devil to become Chainsawman.</Text>
		</View>
	);
}
