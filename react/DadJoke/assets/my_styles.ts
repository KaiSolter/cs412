// react/DadJoke/assets/my_styles.ts 
// Author: Kai Solter
// This is a stylesheet for the app, defining common styles for text and images
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  textContainer: {
    alignItems: 'center',
  },
  titleText: {
    fontSize: 20,
    fontWeight: 'bold',
    color : 'white',
  },
  subTitleText: {
    fontSize: 16,
    color : 'white',
  },
  paragraphText: {
    fontSize: 14,
    color : 'white',
  },
  image: {
    width: 180,
    height: 180,
  },
  wideImage: {
    width: 300,
    height: 200,
  }
});

export default styles;