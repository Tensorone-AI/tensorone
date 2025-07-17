/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			fontFamily: {
				inter: ['Inter', 'sans-serif'],
				satoshi: ['Satoshi', 'sans-serif'],
				'dm-sans': ['DM Sans', 'sans-serif'],
				tasa: ['TASA Orbiter Display', 'sans-serif'],
				iosevka: ['Iosevka Term SS01', 'monospace']
			},

			colors: {
				utama: '#23F784',
				kedua: '#00200F',
				ketiga: '#141414',
				abu: '#9D9D9D',
				gradient__green: '#64FCBC',
				abu_abu: '#272727',
				gradient__title: '#1EF664',
				true: '#BCBCBC',
				false: '#525252'
			},
			backgroundImage: {
				'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))'
			},
			screens: {
				'tablet-only': { min: '20rem', max: '47.999rem' },
				'3xl': '118rem'
			}
		}
	},
	daisyui: {
		themes: [
			{
				light: {
					primary: '#2b49ff',
					secondary: '#00b5b4',
					accent: '#ff301c',
					neutral: '#0f1023',
					'base-100': '#fff',
					'base-200': '#f6f7fb',
					'base-300': '#fafbfc',
					info: '#98d7f0',
					success: '#9cdcc5',
					warning: '#ef4444',
					error: '#f8bbb0'
				}
			},
			{
				dark: {
					primary: '#23F784',
					secondary: '#00200F',
					accent: '#ff301c',
					neutral: '#23F784',
					'base-100': '#0B0B0B',
					'base-200': '#000000',
					'base-300': '#181818',
					info: '#98d7f0',
					success: '#9cdcc5',
					warning: '#ef4444',
					error: '#f8bbb0'
				}
			}
		]
	},
	plugins: [require('daisyui')]
};
