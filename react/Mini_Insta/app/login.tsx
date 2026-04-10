import { useEffect, useState } from 'react';
import { Alert, Pressable, Text, TextInput, View } from 'react-native';
import { useRouter } from 'expo-router';

import styles from '../assets/my_styles';
import { useAuth } from '@/context/AuthContext';

const API_BASE_URL = 'https://cs-webapps.bu.edu/ksolter/mini_insta/api';

type LoginResponse = {
  token: string;
};

export default function LoginScreen() {
  const router = useRouter();
  const { token, setToken } = useAuth();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (token) {
      router.replace('/(tabs)/feed');
    }
  }, [token, router]);

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      Alert.alert('Missing fields', 'Please enter both username and password.');
      return;
    }

    try {
      setIsSubmitting(true);

      const response = await fetch(`${API_BASE_URL}/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username.trim(),
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data?.token) {
        throw new Error(data?.error ?? 'Login failed.');
      }

      const loginData = data as LoginResponse;
      setToken(loginData.token);
      router.replace('/(tabs)/feed');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Something went wrong.';
      Alert.alert('Login error', message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <View style={styles.mediumContainer}>
      <View style={styles.titleContainer}>
        <Text style={styles.titleText}>Mini Insta Login</Text>
      </View>

      <View style={styles.smallContainer}>
        <Text style={styles.paragraphText}>Username</Text>
        <View style={styles.inputboxcontainer}>
          <TextInput
            value={username}
            onChangeText={setUsername}
            autoCapitalize="none"
            style={styles.inputbox}
            placeholder="username"
          />
        </View>

        <Text style={styles.paragraphText}>Password</Text>
        <View style={styles.inputboxcontainer}>
          <TextInput
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            style={styles.inputbox}
            placeholder="password"
          />
        </View>

        <Pressable
          onPress={handleLogin}
          style={({ pressed }) => [
            styles.submitButton,
            pressed ? styles.submitButtonPressed : null,
          ]}
          disabled={isSubmitting}
        >
          <Text style={styles.submitButtonText}>{isSubmitting ? 'Signing in...' : 'Sign In'}</Text>
        </Pressable>
      </View>
    </View>
  );
}
