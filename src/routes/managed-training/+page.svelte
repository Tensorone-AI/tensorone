<script>
	// ===================================
	// IMPORTS & STATIC CONFIGURATIONS
	// ===================================
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import CheckIcon from './CheckIcon.svelte';
	import CheckIconCard from './CheckIconCard.svelte';
	import XIcon from './XIcon.svelte';
	import XIconCard from './XIconCard.svelte';
	import ManagedTrainingHeader from './ManagedTrainingHeader.svelte';
	import PlanCard from './PlanCard.svelte';
	import ComparisonTable from './ComparisonTable.svelte';
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { wallet } from '$lib/stores/wallet';

	// Plan configuration - centralized for easy maintenance
	const plans = [
		{
			id: 'basic',
			name: 'Basic',
			price: 490,
			productName: 'Managed Training - Basic',
			description: 'Let Us Train Your AI Model',
			amount: '2.00',
			buttonText: 'Get Started',
			features: [
				{ name: 'Basic training algorithms', included: true },
				{ name: 'Basic GPU support', included: true },
				{ name: 'Basic version control', included: true },
				{ name: 'Hyperparameter Optimization', included: false },
				{ name: 'Model Optimization', included: false },
				{ name: 'CI/CD Integration', included: false },
				{ name: 'Dedicated Account Manager', included: false }
			]
		},
		{
			id: 'business',
			name: 'Business',
			price: 4900,
			productName: 'Managed Training - Business',
			description: 'Let Us Train Your AI Model',
			amount: '4900.00',
			buttonText: 'Get Started',
			features: [
				{ name: 'Basic training algorithms', included: true },
				{ name: 'Basic GPU support', included: true },
				{ name: 'Basic version control', included: true },
				{ name: 'Hyperparameter Optimization', included: true },
				{ name: 'Model Optimization', included: true },
				{ name: 'CI/CD Integration', included: false },
				{ name: 'Dedicated Account Manager', included: false }
			]
		},
		{
			id: 'advanced',
			name: 'Advanced',
			price: 9900,
			productName: 'Managed Training - Advance',
			description: 'Let Us Train Your AI Model',
			amount: '9900.00',
			buttonText: 'Get Started',
			features: [
				{ name: 'Basic training algorithms', included: true },
				{ name: 'Basic GPU support', included: true },
				{ name: 'Basic version control', included: true },
				{ name: 'Hyperparameter Optimization', included: true },
				{ name: 'Model Optimization', included: true },
				{ name: 'CI/CD Integration', included: true },
				{ name: 'Dedicated Account Manager', included: false }
			]
		},
		{
			id: 'enterprise',
			name: 'Enterprise',
			price: null,
			productName: 'Managed Training - Enterprise',
			description: 'Let Us Train Your AI Model',
			amount: null,
			buttonText: 'Get Started',
			priceDisplay: "Let's Talk",
			features: [
				{ name: 'Basic training algorithms', included: true },
				{ name: 'Basic GPU support', included: true },
				{ name: 'Basic version control', included: true },
				{ name: 'Hyperparameter Optimization', included: true },
				{ name: 'Model Optimization', included: true },
				{ name: 'CI/CD Integration', included: true },
				{ name: 'Dedicated Account Manager', included: true }
			]
		}
	];

	// Comparison table data - structured for easier maintenance
	const comparisonData = [
		{
			feature: 'AI Model Development',
			basic: 'Basic training algorithms',
			business: 'Advanced model architectures',
			advanced: 'Advanced model architectures',
			enterprise: 'Customized solutions with bespoke algorithms'
		},
		{
			feature: 'Hyperparameter Optimization',
			basic: false,
			business: true,
			advanced: true,
			enterprise: true
		},
		{
			feature: 'Model Optimization',
			basic: false,
			business: true,
			advanced: true,
			enterprise: 'Customizable upon request'
		},
		{
			feature: 'Support Channels',
			basic: 'Email',
			business: 'Priority email and chat',
			advanced: '24/7 Priority support',
			enterprise: '24/7 Priority support'
		},
		{
			feature: 'Performance Monitoring',
			basic: false,
			business: true,
			advanced: true,
			enterprise: 'Performance Logging API'
		},
		{
			feature: 'Model Deployment Support',
			basic: false,
			business: 'Limited support',
			advanced: 'Dedicated support',
			enterprise: 'Comprehensive deployment assistance'
		},
		{
			feature: 'Dedicated Account Manager',
			basic: false,
			business: false,
			advanced: true,
			enterprise: true
		},
		{
			feature: 'Training Hours per Month',
			basic: 'Up to 200',
			business: 'Up to 700',
			advanced: 'Custom',
			enterprise: 'Custom'
		},
		{
			feature: 'Custom Pipelines',
			basic: false,
			business: false,
			advanced: false,
			enterprise: 'Available upon request'
		},
		{
			feature: 'Response Time',
			basic: '48 hours',
			business: '24 hours',
			advanced: '12 hours',
			enterprise: '1 hour'
		},
		{
			feature: 'AI Frameworks Supported',
			basic: 'TensorFlow, PyTorch',
			business: 'TensorFlow, PyTorch, Keras',
			advanced: 'Customizable based on project requirements',
			enterprise: 'Customizable based on project requirements'
		},
		{
			feature: 'GPU Acceleration',
			basic: false,
			business: 'Enhanced GPU acceleration',
			advanced: 'Enhanced GPU acceleration',
			enterprise: 'Custom GPU setups'
		},
		{
			feature: 'Model Evaluation Metrics',
			basic: 'Basic accuracy and loss',
			business: 'Advanced evaluation metrics',
			advanced: 'Advanced evaluation metrics',
			enterprise: 'Custom evaluation metrics and benchmarks'
		},
		{
			feature: 'AutoML Integration',
			basic: false,
			business: 'Optional',
			advanced: true,
			enterprise: true
		},
		{
			feature: 'Model Versioning',
			basic: 'Basic version control',
			business: 'Versioning and tracking features',
			advanced: 'Advanced versioning and collaboration tools',
			enterprise: 'Advanced versioning and collaboration tools'
		},
		{
			feature: 'CI/CD Integration',
			basic: false,
			business: 'Optional',
			advanced: true,
			enterprise: true
		},
		{
			feature: 'Data Augmentation',
			basic: 'Basic augmentation techniques',
			business: 'Advanced data augmentation methods',
			advanced: 'Custom data augmentation pipelines',
			enterprise: 'Custom data augmentation pipelines'
		},
		{
			feature: 'Transfer Learning Support',
			basic: 'Limited support',
			business: 'Enhanced transfer learning features',
			advanced: 'Enhanced transfer learning features',
			enterprise: 'Customized transfer learning pipelines'
		},
		{
			feature: 'Continuous Training',
			basic: false,
			business: 'Optional',
			advanced: true,
			enterprise: true
		},
		{
			feature: 'Multi-node Training',
			basic: false,
			business: 'Optional',
			advanced: true,
			enterprise: true
		},
		{
			feature: 'Federated Learning',
			basic: false,
			business: false,
			advanced: 'Optional',
			enterprise: true
		},
		{
			feature: 'Model Compression',
			basic: false,
			business: 'Optional',
			advanced: true,
			enterprise: true
		},
		{
			feature: 'Explainable AI',
			basic: false,
			business: 'Optional',
			advanced: true,
			enterprise: true
		},
		{
			feature: 'Privacy-Preserving AI',
			basic: false,
			business: false,
			advanced: 'Available upon request',
			enterprise: true
		},
		{
			feature: 'Model Serving',
			basic: 'Basic model serving',
			business: 'Advanced model serving',
			advanced: 'Advanced model serving',
			enterprise: 'Custom model serving solutions'
		},
		{
			feature: 'Collaborative Development',
			basic: false,
			business: 'Limited',
			advanced: 'Comprehensive collaboration tools',
			enterprise: 'Comprehensive collaboration tools'
		},
		{
			feature: 'Cost Optimization',
			basic: false,
			business: 'Advanced cost optimization',
			advanced: 'Advanced cost optimization',
			enterprise: 'Custom cost optimization strategies'
		},
		{
			feature: 'Compliance & Governance',
			basic: false,
			business: 'Enhanced governance and compliance',
			advanced: 'Enhanced governance and compliance',
			enterprise: 'Custom compliance frameworks'
		}
	];

	export let data = {};

	// Derive address from data or wallet store
	$: address = data?.address || $wallet?.address || '';

	// Utility functions for UI rendering
	function renderComparisonCell(value) {
		if (typeof value === 'boolean') {
			return { type: 'boolean', value };
		}
		return { type: 'text', value };
	}
</script>

<svelte:head>
	<title>Managed Training</title>
	<meta
		name="description"
		content="Enhance your AI models with Tensorone's Managed Training Solutions. Benefit from expert training and detailed price comparisons across Basic, Business, Advanced, and Enterprise plans."
	/>
</svelte:head>

<Header />

<section class="min-h-screen w-full shadow-sm relative p-10">
	<PageTitle subtitle="Managed Training" title="Training Options" {address} />

	<div
		class="p-10"
		in:fade|global={{ delay: 300, duration: 500 }}
		out:fade|global={{ duration: 300 }}
	>
		<ManagedTrainingHeader />

		<!-- Plans Cards -->
		<div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4 mb-8 border-b border-[#444A61] pb-8">
			{#each plans as plan, index}
				<PlanCard {plan} {index} {fly} {quintOut} {CheckIconCard} {XIconCard} />
			{/each}
		</div>

		<!-- Comparison Table -->
		<ComparisonTable {plans} {comparisonData} {renderComparisonCell} {CheckIcon} {XIcon} {fade} />
	</div>
</section>
