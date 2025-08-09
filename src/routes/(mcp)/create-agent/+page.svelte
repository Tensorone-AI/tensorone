<script>
	// =====================================
	// IMPORTS & DEPENDENCIES
	// =====================================
	import { goto } from '$app/navigation';
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import Welcome from './Welcome.svelte';
	import McpServer from './McpServer.svelte';
	import Framework from './Framework.svelte';
	import AiModel from './AiModel.svelte';
	import KnowledgeBase from './KnowledgeBase.svelte';
	import AiVoice from './AiVoice.svelte';
	import AiCharacterDetails from './AiCharacterDetails.svelte';
	import AgentBehavior from './AgentBehavior.svelte';
	import AiFinalize from './AiFinalize.svelte';
	import InfoModal from './InfoModal.svelte';
	import { wallet } from '$lib/stores/wallet';
	import { supabase } from '$lib/db/supabaseClient.js';

	// Logo imports
	import openaiLogo from '$lib/img/open-ai.svg';
	import geminiLogo from '$lib/img/gemini.svg';
	import anthropicLogo from '$lib/img/anthropic.svg';
	import moonshotLogo from '$lib/img/moonshot.svg';
	import langchainLogo from '$lib/img/langchain.svg';
	import crewaiLogo from '$lib/img/crew-ai.svg';
	import microsoftLogo from '$lib/img/microsoft.svg';
	import haystackLogo from '$lib/img/haystack.svg';

	// Icon imports
	import reasoningIcon from '$lib/img/reasoning-icon.svg';
	import actingIcon from '$lib/img/acting-icon.svg';
	import observingIcon from '$lib/img/observing-icon.svg';
	import planningIcon from '$lib/img/planning-icon.svg';
	import collaboratingIcon from '$lib/img/collaborating-icon.svg';
	import selfrefiningIcon from '$lib/img/self-refining-icon.svg';

	// =====================================
	// PROPS & INITIAL DATA
	// =====================================
	export let data = {};

	// =====================================
	// 1. FETCHING FROM DATABASE
	// =====================================

	// Section configuration - would typically come from database
	const sections = [
		{ id: 'welcome', title: 'Welcome', component: Welcome },
		{ id: 'mcpServer', title: 'MCP Server', component: McpServer },
		{ id: 'framework', title: 'Framework', component: Framework },
		{ id: 'aiModel', title: 'AI Model', component: AiModel },
		{ id: 'knowledgeBase', title: 'Knowledge Base', component: KnowledgeBase },
		{ id: 'aiVoice', title: 'AI Voice', component: AiVoice },
		{ id: 'aiCharacterDetails', title: 'Character Details', component: AiCharacterDetails },
		{ id: 'agentBehavior', title: 'Agent Behavior', component: AgentBehavior },
		{ id: 'aiFinalize', title: 'Finalize', component: AiFinalize }
	];

	// MCP Servers data - would typically be fetched from database
	const mcpServers = [
		{
			id: 'news-aggregator-mcp',
			name: 'News Aggregator MCP',
			description:
				'Real-time news aggregation from multiple global sources including Reuters, AP, BBC, and regional news outlets. Provides categorized news feeds, trending topics analysis, and sentiment scoring.',
			cost: 85,
			features: [
				'Real-time news aggregation from 50+ sources',
				'Advanced sentiment analysis and topic categorization',
				'Multi-language support (15+ languages)',
				'Custom news filtering and alerts',
				'Historical news archive access',
				'Trending topics detection'
			]
		},
		{
			id: 'weather-analytics-mcp',
			name: 'Weather Analytics MCP',
			description:
				'Comprehensive weather data service providing current conditions, forecasts, and climate analytics. Integrates with major weather APIs and provides predictive modeling capabilities.',
			cost: 65,
			features: [
				'Global weather data coverage',
				'7-day detailed forecasts',
				'Severe weather alerts and notifications',
				'Historical weather data analysis',
				'Climate pattern recognition',
				'Agricultural weather insights'
			]
		},
		{
			id: 'social-media-mcp',
			name: 'Social Media Insights MCP',
			description:
				'Monitor and analyze social media trends across platforms. Track brand mentions, sentiment analysis, influencer identification, and viral content detection with real-time processing.',
			cost: 120,
			features: [
				'Multi-platform monitoring (Twitter, Instagram, TikTok)',
				'Real-time sentiment analysis',
				'Influencer identification and ranking',
				'Viral content prediction algorithms',
				'Brand mention tracking',
				'Competitor analysis dashboard'
			]
		},
		{
			id: 'financial-data-mcp',
			name: 'Financial Data MCP',
			description:
				'Access to real-time financial markets data, cryptocurrency prices, economic indicators, and trading analytics. Includes portfolio tracking and risk assessment tools.',
			cost: 150,
			features: [
				'Real-time stock and crypto market data',
				'Economic indicators and analysis',
				'Portfolio performance tracking',
				'Risk assessment algorithms',
				'Technical analysis indicators',
				'Market sentiment analysis'
			]
		}
	];

	// AI Models data - would typically be fetched from database
	const aiModels = [
		{
			id: 'openai',
			name: 'OpenAI',
			logo: openaiLogo,
			models: [
				{ id: 'gpt-4o', name: 'GPT-4o', cost: 95 },
				{ id: 'gpt-4o-mini', name: 'GPT-4o Mini', cost: 25 },
				{ id: 'gpt-4', name: 'GPT-4', cost: 85 },
				{ id: 'gpt-3.5', name: 'GPT-3.5', cost: 15 },
				{ id: 'openai-o1', name: 'OpenAI o1', cost: 120 }
			]
		},
		{
			id: 'Moonshot',
			name: 'Moonshot',
			logo: moonshotLogo,
			models: [
				{ id: 'kimi-k2', name: 'Kimi K2', cost: 45 },
				{ id: 'kimi-k1.5', name: 'Kimi K1.5', cost: 25 }
			]
		},
		{
			id: 'google',
			name: 'Google',
			logo: geminiLogo,
			models: [
				{ id: 'gemini-2.5-pro', name: 'Gemini 2.5 Pro', cost: 90 },
				{ id: 'gemini-2.5-flash', name: 'Gemini 2.5 Flash', cost: 35 },
				{ id: 'gemini-2.0-flash', name: 'Gemini 2.0 Flash', cost: 30 }
			]
		},
		{
			id: 'anthropic',
			name: 'Anthropic',
			logo: anthropicLogo,
			models: [
				{ id: 'claude-3.7-haiku', name: 'Claude 3.7 Haiku', cost: 20 },
				{ id: 'claude-3.5-sonnet', name: 'Claude 3.5 Sonnet', cost: 75 }
			]
		}
	];

	// Frameworks data - would typically be fetched from database
	const frameworks = [
		{
			id: 'langchain',
			name: 'LangChain',
			logo: langchainLogo,
			bestFor: 'Tool-heavy agents, custom pipelines',
			downside:
				'Can become overly complex. Requires careful design to avoid performance and maintenance issues.',
			cost: 45
		},
		{
			id: 'crewai',
			name: 'CrewAI',
			logo: crewaiLogo,
			bestFor: 'Multi-agent collaboration',
			downside:
				'Less suited for single-agent or loosely defined tasks. Limited documentation in some areas.',
			cost: 65
		},
		{
			id: 'microsoft-autogen',
			name: 'Microsoft Autogen',
			logo: microsoftLogo,
			bestFor: 'Research-grade agent systems',
			downside:
				'Requires significant setup and coding to get usable behavior. Not ideal for quick prototypes or no-code use.',
			cost: 80
		},
		{
			id: 'haystack',
			name: 'Haystack',
			logo: haystackLogo,
			bestFor: 'RAG-heavy use cases (retrieval-augmented generation)',
			downside:
				'Optimized for retrieval use cases; less flexible for general-purpose. Setup can be heavy for smaller tasks.',
			cost: 55
		}
	];

	// Voice data - would typically be fetched from database
	const voices = [
		{
			category: 'masculine',
			voices: [
				{
					id: 1,
					voiceString:
						's3://voice-cloning-zero-shot/e46b4027-b38d-4d24-b292-38fbca2be0ef/original/manifest.json',
					name: 'Apex',
					cost: 15
				},
				{
					id: 2,
					voiceString:
						's3://voice-cloning-zero-shot/743575eb-efdc-4c10-b185-a5018148822f/original/manifest.json',
					name: 'Felix',
					cost: 12
				},
				{
					id: 3,
					voiceString:
						's3://voice-cloning-zero-shot/7c339a9d-370f-4643-adf5-4134e3ec9886/mlae02/manifest.json',
					name: 'Isaac',
					cost: 18
				}
			]
		},
		{
			category: 'feminine',
			voices: [
				{
					id: 4,
					voiceString:
						's3://voice-cloning-zero-shot/80ba8839-a6e6-470c-8f68-7c1e5d3ee2ff/abigailsaad/manifest.json',
					name: 'Avarice',
					cost: 16
				},
				{
					id: 5,
					voiceString:
						's3://voice-cloning-zero-shot/f6c4ed76-1b55-4cd9-8896-31f7535f6cdb/original/manifest.json',
					name: 'Archive',
					cost: 14
				},
				{
					id: 6,
					voiceString:
						's3://voice-cloning-zero-shot/90217770-a480-4a91-b1ea-df00f4d4c29d/original/manifest.json',
					name: 'Rose',
					cost: 13
				}
			]
		},
		{
			category: 'machine',
			voices: [
				{
					id: 7,
					voiceString:
						's3://voice-cloning-zero-shot/a540a448-a9ca-446c-9538-d1bae6c506f1/original/manifest.json',
					name: 'Prometheus',
					cost: 20
				},
				{
					id: 8,
					voiceString:
						's3://voice-cloning-zero-shot/dc90b58b-59a9-4e65-955d-c7620deb2d7a/original/manifest.json',
					name: 'Caesium',
					cost: 22
				},
				{
					id: 9,
					voiceString:
						's3://voice-cloning-zero-shot/f43cc4b4-b193-4a13-a903-e6b125c3d572/original/manifest.json',
					name: 'Sumatra',
					cost: 19
				}
			]
		}
	];

	const tempoOptions = [
		{ id: 'slow', name: 'Slow', cost: 5 },
		{ id: 'normal', name: 'Normal', cost: 0 },
		{ id: 'fast', name: 'Fast', cost: 3 },
		{ id: 'very-fast', name: 'Very Fast', cost: 8 }
	];

	const styleOptions = [
		{ id: 'conversational', name: 'Conversational', cost: 0 },
		{ id: 'professional', name: 'Professional', cost: 5 },
		{ id: 'friendly', name: 'Friendly', cost: 3 },
		{ id: 'authoritative', name: 'Authoritative', cost: 7 },
		{ id: 'empathetic', name: 'Empathetic', cost: 6 }
	];

	// Character details configuration - would typically come from database
	const characterDetailsCosts = {
		memory: {
			enableMemory: 25,
			referenceSavedMemories: 15,
			referenceChatHistory: 10,
			shareDataToUs: 5,
			frequency: {
				low: 5,
				medium: 10,
				high: 20,
				realtime: 35
			}
		}
	};

	const memoryFrequencies = [
		{ id: 'low', name: 'Low', description: 'Minimal memory processing' },
		{ id: 'medium', name: 'Medium', description: 'Balanced memory processing' },
		{ id: 'high', name: 'High', description: 'Enhanced memory processing' },
		{ id: 'realtime', name: 'Real-time', description: 'Continuous memory processing' }
	];

	const agentTones = [
		{ id: 'professional', name: 'Professional', description: 'Business-like tone' },
		{ id: 'friendly', name: 'Friendly', description: 'Warm and approachable' },
		{ id: 'casual', name: 'Casual', description: 'Relaxed and informal' },
		{ id: 'enthusiastic', name: 'Enthusiastic', description: 'Energetic and excited' },
		{ id: 'empathetic', name: 'Empathetic', description: 'Understanding and caring' },
		{ id: 'analytical', name: 'Analytical', description: 'Data-driven and logical' }
	];

	// Agent behavior configuration - would typically come from database
	const behaviorCategories = [
		{
			id: 'reasoning',
			name: 'Reasoning',
			icon: reasoningIcon,
			options: [
				{ key: 'approach', options: ['bold', 'safe'] },
				{ key: 'method', options: ['heuristic', 'logical'] },
				{ key: 'style', options: ['flexible', 'structured'] },
				{ key: 'type', options: ['inductive', 'deductive'] }
			]
		},
		{
			id: 'acting',
			name: 'Acting',
			icon: actingIcon,
			options: [
				{ key: 'control', options: ['controlled', 'autonomous'] },
				{ key: 'flexibility', options: ['rigid', 'adaptive'] },
				{ key: 'execution', options: ['manual', 'tool-based'] },
				{ key: 'precision', options: ['exact', 'approximate'] }
			]
		},
		{
			id: 'observing',
			name: 'Observing',
			icon: observingIcon,
			options: [
				{ key: 'mode', options: ['passive', 'active'] },
				{ key: 'depth', options: ['surface', 'deep'] },
				{ key: 'scope', options: ['narrow', 'wide'] },
				{ key: 'attitude', options: ['skeptical', 'accepting'] }
			]
		},
		{
			id: 'planning',
			name: 'Planning',
			icon: planningIcon,
			options: [
				{ key: 'horizon', options: ['short-term', 'long-term'] },
				{ key: 'priority', options: ['perfect', 'fast'] },
				{ key: 'involvement', options: ['active', 'passive'] },
				{ key: 'strategy', options: ['single-path', 'multi-path'] }
			]
		},
		{
			id: 'collaborating',
			name: 'Collaborating',
			icon: collaboratingIcon,
			options: [
				{ key: 'role', options: ['leader', 'team-member'] },
				{ key: 'communication', options: ['negotiator', 'listener'] },
				{ key: 'transparency', options: ['transparent', 'minimal'] },
				{ key: 'adaptation', options: ['fixed', 'dynamic'] }
			]
		},
		{
			id: 'self-refining',
			name: 'Self-Refining',
			icon: selfrefiningIcon,
			options: [
				{ key: 'stability', options: ['stable', 'agile'] },
				{ key: 'feedback', options: ['explicit', 'implicit'] },
				{ key: 'exploration', options: ['conservative', 'curious'] },
				{ key: 'response', options: ['preventative', 'reactive'] }
			]
		}
	];

	// =====================================
	// 2. REACTIVITY ONLY
	// =====================================

	// State management
	let currentSectionIndex = 0;
	let selectedServers = [];
	let selectedFramework = null;
	let selectedModel = null;
	let knowledgeBase = {
		uploadedFiles: [],
		rawData: ''
	};
	let selectedVoice = null;
	let characterDetails = {
		name: '',
		description: '',
		memory: {
			enableMemory: false,
			referenceSavedMemories: false,
			referenceChatHistory: false,
			shareDataToUs: false,
			frequency: ''
		},
		personalization: {
			userName: '',
			agentTone: ''
		}
	};
	let agentBehavior = {};
	let behaviorSelections = {};
	let isLoading = false;
	let selectedRadioValue = null;
	let isVoiceEnabled = false;
	let selectedVoiceId = null;
	let selectedTempo = '';
	let selectedStyle = '';
	let isInfoModalOpen = false;
	let selectedServerForInfo = null;
	let currentPlayingAudio = null;
	let currentPlayingVoice = null;
	let computeUnitsStore = {
		current: 0,
		total: 0,
		available: 0,
		isLoading: true,
		error: null
	};

	// Derived data from props/stores
	$: address = data?.address || $wallet?.address || '';

	// Fetch compute units when address changes
	$: if (address && !$wallet.isLoading) {
		fetchComputeUnits(address);
	} else if (!address) {
		computeUnitsStore = {
			current: 0,
			total: 0,
			available: 0,
			isLoading: false,
			error: null
		};
	}

	// Navigation reactive statements
	$: currentSection = sections[currentSectionIndex];
	$: isFirstSection = currentSectionIndex === 0;
	$: isLastSection = currentSectionIndex === sections.length - 1;

	// Cost calculations
	$: mcpServersCost = mcpServers
		.filter((server) => selectedServers.includes(server.id))
		.reduce((total, server) => total + server.cost, 0);
	$: frameworkCost = selectedFramework?.cost || 0;
	$: modelCost = selectedModel?.cost || 0;
	$: knowledgeBaseCost = (() => {
		let cost = 0;
		// 25 cu per uploaded file
		cost += knowledgeBase.uploadedFiles.length * 25;
		// 25 cu if raw data is provided (regardless of length)
		if (knowledgeBase.rawData.trim() !== '') {
			cost += 25;
		}
		return cost;
	})();

	$: characterDetailsMemoryCost =
		(characterDetails.memory?.enableMemory ? characterDetailsCosts.memory.enableMemory : 0) +
		(characterDetails.memory?.referenceSavedMemories
			? characterDetailsCosts.memory.referenceSavedMemories
			: 0) +
		(characterDetails.memory?.referenceChatHistory
			? characterDetailsCosts.memory.referenceChatHistory
			: 0) +
		(characterDetails.memory?.shareDataToUs ? characterDetailsCosts.memory.shareDataToUs : 0) +
		(characterDetails.memory?.frequency
			? characterDetailsCosts.memory.frequency[characterDetails.memory.frequency] || 0
			: 0);

	$: characterDetailsCost = characterDetailsMemoryCost;

	$: totalVoiceCost = (() => {
		if (!isVoiceEnabled) return 0;
		let total = 0;
		const voice = findVoiceById(selectedVoiceId);
		const tempo = findOptionById(tempoOptions, selectedTempo);
		const style = findOptionById(styleOptions, selectedStyle);
		if (voice) total += voice.cost;
		if (tempo) total += tempo.cost;
		if (style) total += style.cost;
		return total;
	})();

	$: totalNewAgentCost =
		mcpServersCost +
		frameworkCost +
		modelCost +
		knowledgeBaseCost +
		totalVoiceCost +
		characterDetailsCost;

	// Validation reactive statements
	$: characterDetailsMemoryTogglesSelected =
		characterDetails.memory?.referenceSavedMemories ||
		characterDetails.memory?.referenceChatHistory ||
		characterDetails.memory?.shareDataToUs;

	$: isCharacterDetailsFormValid =
		characterDetails.name?.trim() !== '' &&
		characterDetails.description?.trim() !== '' &&
		characterDetails.personalization?.agentTone !== '' &&
		characterDetails.personalization?.userName?.trim() !== '' &&
		(!characterDetails.memory?.enableMemory ||
			(characterDetailsMemoryTogglesSelected && characterDetails.memory?.frequency !== ''));

	$: canProceed = (() => {
		switch (currentSection.id) {
			case 'welcome':
				return true; // Welcome section can always proceed
			case 'mcpServer':
				return selectedServers.length > 0;
			case 'framework':
				return selectedFramework !== null;
			case 'aiModel':
				return selectedModel !== null;
			case 'knowledgeBase':
				return true; // Knowledge base is optional, can always proceed
			case 'aiVoice':
				return (
					!selectedVoice?.enabled ||
					(selectedVoice?.voiceId && selectedVoice?.tempoId && selectedVoice?.styleId)
				);
			case 'aiCharacterDetails':
				return isCharacterDetailsFormValid;
			case 'agentBehavior':
				return agentBehavior.description && agentBehavior.description.trim() !== '';
			case 'aiFinalize':
				return true;
			default:
				return true;
		}
	})();

	$: isVoiceSelected = (voiceId) => selectedVoiceId === voiceId && isVoiceEnabled;

	// Check if there are insufficient compute units
	$: hasInsufficientComputeUnits =
		!computeUnitsStore.isLoading && computeUnitsStore.available < totalNewAgentCost;

	// Reset memory components when enableMemory is disabled
	$: if (!characterDetails.memory?.enableMemory) {
		characterDetails.memory.referenceSavedMemories = false;
		characterDetails.memory.referenceChatHistory = false;
		characterDetails.memory.shareDataToUs = false;
		characterDetails.memory.frequency = '';
	}

	// Initialize behavior selections with defaults
	$: {
		if (Object.keys(agentBehavior).length === 0 && Object.keys(behaviorSelections).length === 0) {
			behaviorCategories.forEach((category) => {
				behaviorSelections[category.id] = {};
				category.options.forEach((option) => {
					behaviorSelections[category.id][option.key] = option.options[0];
				});
			});
			agentBehavior = {
				...behaviorSelections,
				description: generateBehaviorDescription(behaviorSelections, behaviorCategories)
			};
		} else if (
			Object.keys(agentBehavior).length > 0 &&
			Object.keys(behaviorSelections).length === 0
		) {
			behaviorSelections = { ...agentBehavior };
			delete behaviorSelections.description;
		}
	}

	// Component props reactive statements
	$: welcomeProps = {
		isLoading,
		canProceed: canProceed || hasInsufficientComputeUnits, // Always show button
		computeUnitsStore: computeUnitsStore,
		newAgentCost: totalNewAgentCost,
		hasInsufficientComputeUnits,
		nextButtonText: hasInsufficientComputeUnits ? 'Rent More GPU' : 'Next',
		nextButtonClass: hasInsufficientComputeUnits ? 'btn-success' : 'btn-primary'
	};

	$: mcpServerProps = {
		mcpServers,
		selectedServers,
		totalSelectedCost: mcpServersCost,
		isLoading,
		canProceed: canProceed || hasInsufficientComputeUnits,
		computeUnitsStore: computeUnitsStore,
		newAgentCost: totalNewAgentCost,
		hasInsufficientComputeUnits,
		nextButtonText: hasInsufficientComputeUnits ? 'Rent More GPU' : 'Next',
		nextButtonClass: hasInsufficientComputeUnits ? 'btn-success' : 'btn-primary'
	};

	$: frameworkProps = {
		frameworks,
		selectedFramework,
		selectedFrameworkCost: selectedFramework?.cost || 0,
		isLoading,
		canProceed: canProceed || hasInsufficientComputeUnits,
		computeUnitsStore: computeUnitsStore,
		newAgentCost: totalNewAgentCost,
		hasInsufficientComputeUnits,
		nextButtonText: hasInsufficientComputeUnits ? 'Rent More GPU' : 'Next',
		nextButtonClass: hasInsufficientComputeUnits ? 'btn-success' : 'btn-primary'
	};

	$: aiModelProps = {
		aiModels,
		selectedModelCost: selectedModel?.cost || 0,
		selectedRadioValue,
		isLoading,
		canProceed: canProceed || hasInsufficientComputeUnits,
		computeUnitsStore: computeUnitsStore,
		newAgentCost: totalNewAgentCost,
		hasInsufficientComputeUnits,
		nextButtonText: hasInsufficientComputeUnits ? 'Rent More GPU' : 'Next',
		nextButtonClass: hasInsufficientComputeUnits ? 'btn-success' : 'btn-primary'
	};

	$: knowledgeBaseProps = {
		knowledgeBase,
		selectedKnowledgeBaseCost: knowledgeBaseCost,
		isLoading,
		canProceed: canProceed || hasInsufficientComputeUnits,
		computeUnitsStore: computeUnitsStore,
		newAgentCost: totalNewAgentCost,
		hasInsufficientComputeUnits,
		nextButtonText: hasInsufficientComputeUnits ? 'Rent More GPU' : 'Next',
		nextButtonClass: hasInsufficientComputeUnits ? 'btn-success' : 'btn-primary',
		formatFileSize,
		handleBrowseClick
	};

	$: aiVoiceProps = {
		voices,
		tempoOptions,
		styleOptions,
		isVoiceEnabled,
		selectedTempo,
		selectedStyle,
		totalVoiceCost,
		isLoading,
		canProceed: canProceed || hasInsufficientComputeUnits,
		computeUnitsStore: computeUnitsStore,
		newAgentCost: totalNewAgentCost,
		hasInsufficientComputeUnits,
		nextButtonText: hasInsufficientComputeUnits ? 'Rent More GPU' : 'Next',
		nextButtonClass: hasInsufficientComputeUnits ? 'btn-success' : 'btn-primary',
		isVoiceSelected,
		handlePlayVoice,
		currentPlayingVoice
	};

	$: aiCharacterDetailsProps = {
		characterDetails,
		characterDetailsCost,
		memoryFrequencies,
		agentTones,
		isCharacterDetailsFormValid,
		isLoading,
		canProceed: canProceed || hasInsufficientComputeUnits,
		computeUnitsStore: computeUnitsStore,
		newAgentCost: totalNewAgentCost,
		hasInsufficientComputeUnits,
		nextButtonText: hasInsufficientComputeUnits ? 'Rent More GPU' : 'Next',
		nextButtonClass: hasInsufficientComputeUnits ? 'btn-success' : 'btn-primary'
	};

	$: agentBehaviorProps = {
		behaviorSelections,
		behaviorCategories,
		isLoading,
		canProceed: canProceed || hasInsufficientComputeUnits,
		computeUnitsStore: computeUnitsStore,
		newAgentCost: totalNewAgentCost,
		hasInsufficientComputeUnits,
		nextButtonText: hasInsufficientComputeUnits ? 'Rent More GPU' : 'Next',
		nextButtonClass: hasInsufficientComputeUnits ? 'btn-success' : 'btn-primary',
		capitalize
	};

	$: aiFinalizeProps = {
		selectedServers,
		selectedFramework,
		selectedModel,
		knowledgeBase,
		selectedVoice,
		characterDetails,
		agentBehavior,
		totalCost: totalNewAgentCost,
		isLoading,
		canProceed: canProceed || hasInsufficientComputeUnits,
		computeUnitsStore: computeUnitsStore,
		newAgentCost: totalNewAgentCost,
		hasInsufficientComputeUnits,
		nextButtonText: hasInsufficientComputeUnits ? 'Rent More GPU' : 'Finalize',
		nextButtonClass: hasInsufficientComputeUnits ? 'btn-success' : 'btn-primary',
		mcpServersCost,
		frameworkCost,
		modelCost,
		knowledgeBaseCost,
		voiceCost: totalVoiceCost,
		characterDetailsCost,
		getServerNameById,
		getAgentToneName,
		formatVoiceSettings,
		formatMemorySettings,
		formatBehaviorCategory
	};

	// =====================================
	// UTILITY FUNCTIONS
	// =====================================

	async function fetchComputeUnits(address) {
		if (!address) return;

		computeUnitsStore = { ...computeUnitsStore, isLoading: true, error: null };

		try {
			// Fetch compute units from GPU table
			const { data: gpuData, error: gpuError } = await supabase
				.from('gpu')
				.select('compute')
				.eq('address', address);

			if (gpuError) {
				throw gpuError;
			}

			// Fetch used compute units from MCP table
			const { data: mcpData, error: mcpError } = await supabase
				.from('mcp')
				.select('total_cu')
				.eq('address', address);

			if (mcpError) {
				throw mcpError;
			}

			// Sum all compute values from GPU table (total available)
			const totalCompute = gpuData?.reduce((sum, row) => sum + (row.compute || 0), 0) || 0;

			// Sum all used compute units from MCP table
			const usedCompute = mcpData?.reduce((sum, row) => sum + (row.total_cu || 0), 0) || 0;

			computeUnitsStore = {
				current: usedCompute, // Current usage from MCP agents
				total: totalCompute,
				available: totalCompute - usedCompute, // Available = total - used
				isLoading: false,
				error: null
			};
		} catch (error) {
			console.error('Error fetching compute units:', error);
			computeUnitsStore = {
				current: 0,
				total: 0,
				available: 0,
				isLoading: false,
				error: error.message
			};
		}
	}

	function findVoiceById(voiceId) {
		if (!voiceId) return null;
		for (const category of voices) {
			const voice = category.voices.find((v) => v.id === voiceId);
			if (voice) return voice;
		}
		return null;
	}

	function findOptionById(options, optionId) {
		return options.find((option) => option.id === optionId) || null;
	}

	function getServerNameById(serverId) {
		const server = mcpServers.find((s) => s.id === serverId);
		return server ? server.name : serverId;
	}

	function getVoiceNameById(voiceId) {
		if (voiceId === null || voiceId === undefined) return null;
		for (const category of voices) {
			const voice = category.voices.find((v) => v.id === voiceId);
			if (voice) return voice.name;
		}
		return `Voice ${voiceId}`;
	}

	function getOptionNameById(options, optionId) {
		const option = options.find((opt) => opt.id === optionId);
		return option ? option.name : optionId;
	}

	function getMemoryFrequencyName(frequencyId) {
		const frequency = memoryFrequencies.find((f) => f.id === frequencyId);
		return frequency ? frequency.name : frequencyId;
	}

	function getAgentToneName(toneId) {
		const tone = agentTones.find((t) => t.id === toneId);
		return tone ? tone.name : toneId;
	}

	function formatVoiceSettings(voice) {
		if (!voice || !voice.enabled) return 'Voice disabled';
		const parts = [];
		if (voice.voiceId) {
			const voiceName = getVoiceNameById(voice.voiceId);
			if (voiceName) parts.push(voiceName);
		}
		if (voice.tempoId) {
			const tempoName = getOptionNameById(tempoOptions, voice.tempoId);
			if (tempoName) parts.push(tempoName);
		}
		if (voice.styleId) {
			const styleName = getOptionNameById(styleOptions, voice.styleId);
			if (styleName) parts.push(styleName);
		}
		return parts.length > 0 ? parts.join(', ') : 'Voice enabled';
	}

	function getVoiceFilePath(voiceId) {
		return `/samples/voice-${voiceId}.wav`;
	}

	function formatMemorySettings(memory) {
		if (!memory || !memory.enableMemory) return 'Memory disabled';
		const settings = [];
		if (memory.referenceSavedMemories) settings.push('Reference Memories');
		if (memory.referenceChatHistory) settings.push('Reference Chat');
		if (memory.shareDataToUs) settings.push('Share Data');
		if (memory.frequency) {
			const frequencyName = getMemoryFrequencyName(memory.frequency);
			settings.push(`Frequency: ${frequencyName}`);
		}
		return settings.length > 0 ? settings.join(', ') : 'Memory enabled';
	}

	function formatBehaviorCategory(categoryData, categoryName) {
		if (!categoryData) return [];
		const behaviors = [];
		for (const [key, value] of Object.entries(categoryData)) {
			if (key !== 'description') {
				const formattedValue = value
					.split('-')
					.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
					.join(' ');
				behaviors.push(formattedValue);
			}
		}
		return behaviors;
	}

	function capitalize(str) {
		return str.charAt(0).toUpperCase() + str.slice(1);
	}

	function generateBehaviorDescription(selections, categories) {
		const descriptions = [];
		categories.forEach((category) => {
			const categorySelections = selections[category.id] || {};
			const options = Object.values(categorySelections).join(', ');
			descriptions.push(`${category.name}: ${options}`);
		});
		return descriptions.join(' | ');
	}

	// Knowledge Base utility functions
	function formatFileSize(bytes) {
		if (bytes === 0) return '0 Bytes';
		const k = 1024;
		const sizes = ['Bytes', 'KB', 'MB', 'GB'];
		const i = Math.floor(Math.log(bytes) / Math.log(k));
		return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
	}

	function handleBrowseClick(fileInput) {
		fileInput?.click();
	}

	function handlePlayVoice(voiceId) {
		if (!isVoiceEnabled) return;

		// Stop any currently playing audio
		if (currentPlayingAudio) {
			currentPlayingAudio.pause();
			currentPlayingAudio.currentTime = 0;
			currentPlayingAudio = null;
			currentPlayingVoice = null;
		}

		// Create new audio element
		const audioFilePath = getVoiceFilePath(voiceId);
		const audio = new Audio(audioFilePath);

		// Set up event listeners
		audio.onloadstart = () => {
			currentPlayingAudio = audio;
			currentPlayingVoice = voiceId;
		};

		audio.onended = () => {
			currentPlayingAudio = null;
			currentPlayingVoice = null;
		};

		audio.onerror = (event) => {
			console.error(`Error playing voice sample ${voiceId}:`, event);
			currentPlayingAudio = null;
			currentPlayingVoice = null;
		};

		audio.onpause = () => {
			currentPlayingAudio = null;
			currentPlayingVoice = null;
		};

		// Play the audio
		audio.play().catch((error) => {
			console.error(`Failed to play voice sample ${voiceId}:`, error);
			currentPlayingAudio = null;
			currentPlayingVoice = null;
		});
	}

	// Navigation functions
	function goToNextSection() {
		// If insufficient compute units, redirect to rent GPU page
		if (hasInsufficientComputeUnits) {
			goto('/');
			return;
		}

		if (canProceed && !isLoading) {
			if (isLastSection) {
				handleFinalize();
			} else {
				currentSectionIndex = Math.min(currentSectionIndex + 1, sections.length - 1);
			}
		}
	}

	function goToPreviousSection() {
		if (!isLoading) {
			if (isFirstSection) {
				goto('/my-agents');
			} else {
				currentSectionIndex = Math.max(currentSectionIndex - 1, 0);
			}
		}
	}

	// =====================================
	// 3. DATA INPUT TO DATABASE
	// =====================================

	async function handleFinalize() {
		isLoading = true;

		try {
			// Prepare config object with all agent configuration data
			const config = {
				selectedServers,
				selectedFramework,
				selectedModel,
				knowledgeBase,
				selectedVoice,
				characterDetails,
				agentBehavior,
				createdAt: new Date().toISOString()
			};

			// Prepare voice call data if voice is enabled
			const voiceCall =
				selectedVoice?.enabled && selectedVoice?.voiceId
					? findVoiceById(selectedVoice?.voiceId)?.voiceString
					: null;

			const response = await fetch('/api/mcp/create-my-agent', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					address: $wallet.address,
					agent_name: characterDetails.name || 'Unnamed Agent',
					description: characterDetails.description || 'AI Agent created via TensorOne DApp',
					total_cu: totalNewAgentCost,
					config: config,
					call: voiceCall
				})
			});

			const result = await response.json();

			if (result.success) {
				console.log('Agent created successfully:', result.data);
				goto('/my-agents');
			} else {
				console.error('Failed to create agent:', result.error);
				// You might want to show an error message to the user here
			}
		} catch (error) {
			console.error('Error creating agent:', error);
			// You might want to show an error message to the user here
		} finally {
			isLoading = false;
		}
	}

	// Update functions for database operations
	function updateSelectedVoice() {
		selectedVoice = {
			enabled: isVoiceEnabled,
			voiceId: selectedVoiceId,
			tempoId: selectedTempo,
			styleId: selectedStyle,
			cost: totalVoiceCost
		};
	}

	// Event handlers for user input that will eventually be saved to database
	function handleServerToggle(serverId, isEnabled) {
		if (isEnabled) {
			selectedServers = [...selectedServers, serverId];
		} else {
			selectedServers = selectedServers.filter((id) => id !== serverId);
		}
	}

	function handleFrameworkSelect(framework) {
		selectedFramework = framework;
	}

	function handleModelSelect(model) {
		selectedModel = model;
	}

	function handleRadioValueChange(newRadioValue) {
		selectedRadioValue = newRadioValue;
		const [providerId, ...modelIdParts] = newRadioValue.split('-');
		const modelId = modelIdParts.join('-');
		const provider = aiModels.find((p) => p.id === providerId);
		const model = provider?.models.find((m) => m.id === modelId);
		if (model) {
			selectedModel = {
				id: newRadioValue,
				name: model.name,
				provider: provider.name,
				cost: model.cost
			};
		}
	}

	function handleKnowledgeBaseUpdate(updatedKnowledgeBase) {
		knowledgeBase = { ...knowledgeBase, ...updatedKnowledgeBase };
	}

	// Knowledge Base specific database operations
	function handleFileUpload(files, fileInput) {
		const fileArray = Array.from(files);
		if (fileArray.length > 0) {
			const newFiles = fileArray.map((file) => ({
				id: crypto.randomUUID(), // In real app, this would be generated by database
				name: file.name,
				size: file.size,
				type: file.type,
				file: file // In real app, file would be uploaded to storage service
			}));

			const updatedKnowledgeBase = {
				...knowledgeBase,
				uploadedFiles: [...knowledgeBase.uploadedFiles, ...newFiles]
			};

			handleKnowledgeBaseUpdate(updatedKnowledgeBase);
		}

		// Reset file input
		if (fileInput) {
			fileInput.value = '';
		}
	}

	function handleFileRemove(fileId) {
		// In real app, this would also delete file from storage service
		const updatedKnowledgeBase = {
			...knowledgeBase,
			uploadedFiles: knowledgeBase.uploadedFiles.filter((file) => file.id !== fileId)
		};

		handleKnowledgeBaseUpdate(updatedKnowledgeBase);
	}

	function handleRawDataChange(value) {
		const updatedKnowledgeBase = {
			...knowledgeBase,
			rawData: value
		};

		handleKnowledgeBaseUpdate(updatedKnowledgeBase);
	}

	function handleVoiceSelect(voice) {
		selectedVoice = voice;
	}

	function handleVoiceToggle(enabled) {
		isVoiceEnabled = enabled;
		if (!enabled) {
			selectedVoiceId = null;
			selectedTempo = '';
			selectedStyle = '';
		}
		updateSelectedVoice();
	}

	function handleVoiceIdSelect(voiceId) {
		if (isVoiceEnabled) {
			selectedVoiceId = voiceId;
			updateSelectedVoice();
		}
	}

	function handleTempoChange(tempo) {
		if (isVoiceEnabled) {
			selectedTempo = tempo;
			updateSelectedVoice();
		}
	}

	function handleStyleChange(style) {
		if (isVoiceEnabled) {
			selectedStyle = style;
			updateSelectedVoice();
		}
	}

	function handleCharacterDetailsUpdate(updatedDetails) {
		characterDetails = { ...characterDetails, ...updatedDetails };
	}

	function handleAgentBehaviorUpdate(updatedBehavior) {
		agentBehavior = { ...agentBehavior, ...updatedBehavior };
	}

	function handleBehaviorSelectionUpdate(categoryId, optionKey, selectedValue) {
		behaviorSelections[categoryId][optionKey] = selectedValue;
		agentBehavior = {
			...behaviorSelections,
			description: generateBehaviorDescription(behaviorSelections, behaviorCategories)
		};
	}

	// =====================================
	// EVENT HANDLERS FOR UI INTERACTIONS
	// =====================================

	function handleShowServerInfo(server) {
		selectedServerForInfo = server;
		isInfoModalOpen = true;
	}

	function handleInfoClick(server) {
		handleShowServerInfo(server);
	}

	function handleCloseInfoModal() {
		isInfoModalOpen = false;
		selectedServerForInfo = null;
	}

	function handleEditSection(sectionId) {
		const sectionIndex = sections.findIndex((section) => section.id === sectionId);
		if (sectionIndex !== -1) {
			currentSectionIndex = sectionIndex;
		}
	}

	function handleNext() {
		goToNextSection();
	}

	function handleBack() {
		goToPreviousSection();
	}
</script>

<svelte:head>
	<title>Create New Agent</title>
	<meta name="description" content="Create and configure AI agents with MCP servers" />
</svelte:head>

<Header />

<section class="min-h-screen w-full shadow-sm relative px-10 py-9 flex flex-col">
	<PageTitle subtitle="AI Agents" title="Create your own AI Agent" {address} />

	<!-- Current Section Component -->
	{#if currentSection.id === 'welcome'}
		<Welcome {...welcomeProps} on:next={handleNext} on:back={handleBack} />
	{:else if currentSection.id === 'mcpServer'}
		<McpServer
			{...mcpServerProps}
			on:serverToggle={(e) => handleServerToggle(e.detail.serverId, e.detail.isEnabled)}
			on:showServerInfo={(e) => handleShowServerInfo(e.detail.server)}
			on:next={handleNext}
			on:back={handleBack}
		/>
	{:else if currentSection.id === 'framework'}
		<Framework
			{...frameworkProps}
			on:frameworkSelect={(e) => handleFrameworkSelect(e.detail.framework)}
			on:next={handleNext}
			on:back={handleBack}
		/>
	{:else if currentSection.id === 'aiModel'}
		<AiModel
			{...aiModelProps}
			on:modelSelect={(e) => handleModelSelect(e.detail.model)}
			on:radioValueChange={(e) => handleRadioValueChange(e.detail.radioValue)}
			on:next={handleNext}
			on:back={handleBack}
		/>
	{:else if currentSection.id === 'knowledgeBase'}
		<KnowledgeBase
			{...knowledgeBaseProps}
			on:knowledgeBaseUpdate={(e) => handleKnowledgeBaseUpdate(e.detail)}
			on:fileUpload={(e) => handleFileUpload(e.detail.files, e.detail.fileInput)}
			on:fileRemove={(e) => handleFileRemove(e.detail.fileId)}
			on:rawDataChange={(e) => handleRawDataChange(e.detail.value)}
			on:next={handleNext}
			on:back={handleBack}
		/>
	{:else if currentSection.id === 'aiVoice'}
		<AiVoice
			{...aiVoiceProps}
			on:voiceSelect={(e) => handleVoiceSelect(e.detail.voice)}
			on:voiceToggle={(e) => handleVoiceToggle(e.detail.enabled)}
			on:voiceIdSelect={(e) => handleVoiceIdSelect(e.detail.voiceId)}
			on:tempoChange={(e) => handleTempoChange(e.detail.tempo)}
			on:styleChange={(e) => handleStyleChange(e.detail.style)}
			on:next={handleNext}
			on:back={handleBack}
		/>
	{:else if currentSection.id === 'aiCharacterDetails'}
		<AiCharacterDetails
			{...aiCharacterDetailsProps}
			on:characterDetailsUpdate={(e) => handleCharacterDetailsUpdate(e.detail)}
			on:next={handleNext}
			on:back={handleBack}
		/>
	{:else if currentSection.id === 'agentBehavior'}
		<AgentBehavior
			{...agentBehaviorProps}
			on:agentBehaviorUpdate={(e) => handleAgentBehaviorUpdate(e.detail)}
			on:behaviorSelectionUpdate={(e) =>
				handleBehaviorSelectionUpdate(
					e.detail.categoryId,
					e.detail.optionKey,
					e.detail.selectedValue
				)}
			on:next={handleNext}
			on:back={handleBack}
		/>
	{:else if currentSection.id === 'aiFinalize'}
		<AiFinalize
			{...aiFinalizeProps}
			on:finalize={handleFinalize}
			on:editSection={(e) => handleEditSection(e.detail.sectionId)}
			on:next={handleNext}
			on:back={handleBack}
		/>
	{/if}
</section>

<InfoModal isOpen={isInfoModalOpen} server={selectedServerForInfo} onClose={handleCloseInfoModal} />
