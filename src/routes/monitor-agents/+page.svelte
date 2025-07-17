<script>
	// ===== IMPORTS =====
	import { createEventDispatcher, onDestroy } from 'svelte';
	import { supabase } from '$lib/db/supabaseClient.js';
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import AnalyticsNavigation from './AnalyticsNavigation.svelte';
	import StatsGrid from './StatsGrid.svelte';
	import ChartsGrid from './ChartsGrid.svelte';
	import BottomGrid from './BottomGrid.svelte';
	import RightSidebar from './RightSidebar.svelte';
	import CodePage from './CodePage.svelte';
	import LogsPage from './LogsPage.svelte';
	import { dashboardStore, selectedAgentStore } from './dashboardStore.js';
	import { mockDashboardData } from './mockData.js';
	import { wallet } from '$lib/stores/wallet';
	import { fade } from 'svelte/transition';

	// Props
	export let data = {};

	// ===== EVENT DISPATCHER =====
	const dispatch = createEventDispatcher();

	// ===== STATE VARIABLES =====
	let currentView = 'analytics';
	let isLoadingCodeData = false;
	let codeDataError = null;
	let selectedFileId = null;
	let isFullscreen = false;
	let searchQuery = '';
	let isLoadingDashboard = false;
	let dashboardError = null;

	// Logs state
	let logs = [];
	let filteredLogs = [];
	let selectedLogId = null;
	let autoScroll = true;
	let showTimestamps = true;
	let isStreaming = true;
	let logContainer;
	let streamingInterval;
	let isLoadingLogs = false;
	let logsError = null;
	let autoRefresh = true;
	let refreshInterval = 5000 + Math.random() * 3000;
	let maxLogEntries = 1000;
	let pageVisitTime = null; // Track when user visits the page
	let lastFetchTime = null;

	// AgentStatus uptime state
	let currentTime = new Date();
	let uptimeInterval;
	let dashboardRefreshInterval;

	// Code editor copy state
	let isCopied = false;

	// Filters state
	let filters = {
		level: 'all',
		source: 'all',
		searchQuery: ''
	};

	// Code data state
	let codeData = {
		files: [],
		activeFileId: null,
		lastUpdated: null
	};

	// ===== CENTRALIZED CONFIGURATION =====
	const statusConfig = {
		autoRestart: {
			enabled: { color: 'text-utama', label: 'Enabled' },
			disabled: { color: 'text-red-400', label: 'Disabled' }
		},
		loggingLevel: {
			debug: { color: 'text-blue-400', label: 'Debug' },
			info: { color: 'text-utama', label: 'Info' },
			warn: { color: 'text-yellow-400', label: 'Warn' },
			error: { color: 'text-red-400', label: 'Error' }
		}
	};

	// Navigation configuration
	const navigationTabs = [
		{ id: 'analytics', label: 'Analytics', disabled: false },
		{ id: 'code', label: 'Code', disabled: false },
		{ id: 'logs', label: 'Logs', disabled: false }
	];

	// Log levels for filter options
	const logLevels = ['INFO', 'WARN', 'ERROR', 'DEBUG'];
	const logSources = ['system', 'network', 'agent', 'monitor'];

	const mockCodeData = {
		files: [
			{
				id: 'agent-js',
				name: 'agent.js',
				type: 'javascript',
				content: `// Agent using TensorOne AI SDK
import { TensorAgent } from '@tensorone/ai';
import { logEvent } from './logger.js';
import config from './config.json';

const agent = new TensorAgent({
  apiKey: config.tensorone.apiKey,
  capabilities: config.capabilities
});

export async function handleIntent(intent) {
  logEvent("Received intent", intent);

  try {
    const plan = await agent.plan(intent);
    const result = await agent.execute(plan);

    return {
      status: "success",
      data: result,
      ts: new Date().toISOString()
    };
  } catch (err) {
    logEvent("Intent processing failed", err);
    return {
      status: "error",
      error: err.message
    };
  }
}`,
				isActive: true,
				lastModified: 'Just now',
				size: '2.5 KB'
			},

			{
				id: 'tensorone-client-py',
				name: 'tensorone_client.py',
				type: 'python',
				content: `# Python SDK wrapper
import requests

class TensorOneClient:
    def __init__(self, api_key):
        self.base_url = "https://api.tensorone.ai"
        self.headers = { "Authorization": f"Bearer {api_key}" }

    def plan(self, intent):
        return requests.post(f"{self.base_url}/plan", json=intent, headers=self.headers).json()

    def execute(self, plan):
        return requests.post(f"{self.base_url}/execute", json=plan, headers=self.headers).json()

# Example use:
# client = TensorOneClient("your-token")
# plan = client.plan({ "type": "summarize", "payload": { "text": "long content..." } })`,
				isActive: false,
				lastModified: '1 hour ago',
				size: '1.6 KB'
			},

			{
				id: 'config-json',
				name: 'config.json',
				type: 'json',
				content: `{
  "tensorone": {
    "apiKey": "sk-tensorone-xx"
  },
  "agent": {
    "version": "1.0.41",
    "mode": "dev",
    "logging": true
  },
  "capabilities": [
    "planning",
    "summarization",
    "semantic-search",
    "tool-use",
    "multi-agent-coordination"
  ]
}`,
				isActive: false,
				lastModified: 'Today',
				size: '0.9 KB'
			},

			{
				id: 'readme-md',
				name: 'README.md',
				type: 'markdown',
				content: `# TensorOne Agentic AI

## Powered By
- \`@tensorone/ai\` JavaScript SDK
- \`tensorone\` Python API client
- Mocked endpoint: \`https://api.tensorone.ai\`

## Features
- Intent recognition and planning
- API-based task execution
- Semantic reasoning with external tools
- JS and Python SDKs

## Example
\`\`\`js
import { handleIntent } from './agent.js';

const result = await handleIntent({
  type: "summarize",
  payload: {
    text: "AI agents can coordinate using large language models to perform complex tasks..."
  }
});
console.log(result);
\`\`\`

## Dev Setup
1. Configure \`config.json\` with your API key.
2. Run \`agent.js\` or \`tensorone_client.py\`.`,
				isActive: false,
				lastModified: '2 days ago',
				size: '1.3 KB'
			},

			{
				id: 'types-ts',
				name: 'types.ts',
				type: 'typescript',
				content: `export interface TensorIntent {
  type: string;
  payload: Record<string, any>;
}

export interface AgentResult {
  status: "success" | "error";
  data?: any;
  error?: string;
  ts: string;
}`,
				isActive: false,
				lastModified: 'Yesterday',
				size: '0.5 KB'
			},

			{
				id: 'logger-js',
				name: 'logger.js',
				type: 'javascript',
				content: `export function logEvent(label, payload) {
  if (process.env.NODE_ENV !== 'production') {
    console.log(\`[TENSORONE LOG] \${label}:\`, payload);
  }
}`,
				isActive: false,
				lastModified: '30 minutes ago',
				size: '0.3 KB'
			},

			{
				id: 'test-agent-py',
				name: 'test.py',
				type: 'python',
				content: `#
from tensorone_client import TensorOneClient

client = TensorOneClient("sk-tensorone-xx")

def test_summarize():
    intent = {
        "type": "summarize",
        "payload": { "text": "This is a long article..." }
    }
    plan = client.plan(intent)
    result = client.execute(plan)
    print("Test passed:", result)

if __name__ == "__main__":
    test_summarize()`,
				isActive: false,
				lastModified: 'Just now',
				size: '1.4 KB'
			}
		],
		activeFileId: 'agent-js',
		lastUpdated: new Date().toISOString()
	};

	// ========================================
	// 1. FETCHING FROM DATABASE
	// ========================================

	// Fetch server status data from Supabase
	async function fetchServerStatusFromSupabase() {
		try {
			isLoadingDashboard = true;
			dashboardError = null;

			const { data, error } = await supabase.from('server-status').select('*').single();

			if (error) {
				console.error('Error fetching server status:', error);
				dashboardError = 'Failed to load server status';
				return null;
			}

			if (data) {
				// Transform the data to match mockDashboardData structure
				const transformedData = {
					totalIntents: data['total-intents'] || '0',
					successRate: data['success-rate'] || '0',
					avgResponse: data['avg-response'] || '0',
					activeUsers: data['active-users'] || '0',
					memoryUsage: data['memory-usage'] || '-- MB',
					cpuUsage: data['cpu-usage'] || '--%',
					startedAt: data['started-at']
						? new Date(data['started-at'])
								.toLocaleString('en-GB', {
									day: '2-digit',
									month: '2-digit',
									year: 'numeric',
									hour: '2-digit',
									minute: '2-digit',
									second: '2-digit'
								})
								.replace(',', '')
						: '--/--/----, --:--:--',
					resourceUtilization: data['resource-utilization'] || 0,
					intentVolume: Array.isArray(data['intent-volume']) ? data['intent-volume'] : [0],
					intentCategories: Array.isArray(data['intent-categories'])
						? data['intent-categories']
						: [],
					responseTimeDistribution: Array.isArray(data['response-time-distribution'])
						? data['response-time-distribution']
						: [],
					recentActivity: Array.isArray(data['recent-activity']) ? data['recent-activity'] : [],
					agentDetails: {
						created: data['agent-details']?.created || '--/--/----',
						lastUpdated: data['agent-details']?.lastUpdated || '--/--/----',
						agentId: data['agent-details']?.agentId || '--',
						loggingLevel: data['agent-details']?.loggingLevel || 'Info',
						autoRestart:
							data['agent-details']?.autoRestart !== undefined
								? data['agent-details'].autoRestart
								: true
					}
				};

				return transformedData;
			}
		} catch (err) {
			console.error('Failed to fetch server status from Supabase:', err);
			dashboardError = 'Database connection failed';
		} finally {
			isLoadingDashboard = false;
		}
		return null;
	}

	// Fetch logs from Supabase log-monitor table
	async function fetchLogsFromSupabase() {
		try {
			isLoadingLogs = true;
			logsError = null;

			const currentTime = new Date();

			// Set page visit time if not already set
			if (!pageVisitTime) {
				pageVisitTime = currentTime;
			}

			// Calculate the cutoff time (3 seconds ago from page visit time for first fetch)
			// or from last fetch time for subsequent fetches
			let cutoffTime;
			if (!lastFetchTime) {
				// First fetch: get logs from 3 seconds before page visit
				cutoffTime = new Date(pageVisitTime.getTime() - 3000);
			} else {
				// Subsequent fetches: get logs newer than last fetch time
				cutoffTime = lastFetchTime;
			}

			// Query log-monitor table for newer records
			const { data, error } = await supabase
				.from('log-monitor')
				.select('created_at, level, source, message, details')
				.gt('created_at', cutoffTime.toISOString())
				.order('created_at', { ascending: true });

			if (error) {
				throw error;
			}

			// Transform Supabase data to log format
			if (data && data.length > 0) {
				const newLogs = data.map((record, index) => ({
					id: `log_${record.created_at}_${index}`,
					timestamp: record.created_at,
					level: record.level || 'INFO',
					message: record.message || 'Monitor agent activity',
					source: record.source || 'monitor',
					details: record.details || {},
					agentId: '262316b4',
					agentName: 'Agent'
				}));

				// Add new logs to existing array (cumulative)
				logs = [...logs, ...newLogs];
			}

			// Update last fetch time
			lastFetchTime = currentTime;
		} catch (err) {
			console.error('Failed to fetch logs from Supabase:', err);
			logsError = 'Failed to load logs from database';
		} finally {
			isLoadingLogs = false;
		}
	}

	// Get logs from storage/database
	function getLogsFromStorage() {
		if (typeof window !== 'undefined' && window.agentLogsStore) {
			return window.agentLogsStore['logs_monitor_agent'] || [];
		}
		return [];
	}

	// Load code data from database
	async function loadCodeData() {
		isLoadingCodeData = true;
		codeDataError = null;

		try {
			// TODO: Replace with actual API call to database
			await new Promise((resolve) => setTimeout(resolve, 500));
			console.log('Code data loaded');
		} catch (error) {
			console.error('Failed to load code data:', error);
			codeDataError = 'Failed to load code files';
		} finally {
			isLoadingCodeData = false;
		}
	}

	// Legacy fetch logs function (keeping for compatibility)
	async function fetchLogs() {
		await fetchLogsFromSupabase();
	}

	// Initialize logs data from Supabase
	function initializeLogsData() {
		// Reset logs array and timestamps to start fresh
		logs = [];
		lastFetchTime = null;
		pageVisitTime = new Date(); // Record when user visits the page

		// Fetch initial data from Supabase
		fetchLogsFromSupabase();
	}

	// ========================================
	// 2. REACTIVITY ONLY
	// ========================================

	// Reactive statements for data binding
	const agent = { id: '262316b4', name: 'Monitor Agent', status: 'running' }; // Static agent since we're monitoring server status
	$: selectedAgent = $selectedAgentStore;
	$: dashboardData = $dashboardStore;
	$: address = data?.address || $wallet?.address || '';

	// Display data reactivity
	$: displayCodeData = codeData.files?.length > 0 ? codeData : mockCodeData;
	$: filteredFiles = displayCodeData.files.filter((file) =>
		file.name.toLowerCase().includes(searchQuery.toLowerCase())
	);
	$: activeFile =
		displayCodeData.files.find((file) => file.id === selectedFileId) ||
		displayCodeData.files.find((file) => file.id === displayCodeData.activeFileId) ||
		displayCodeData.files[0];

	// Navigation data reactivity
	$: navigationData = {
		tabs: navigationTabs,
		activeTabId: currentView,
		isLoading: false
	};

	// Badge configurations reactivity
	$: statusBadgeConfig = {
		text: 'Running',
		classes: 'px-4 py-2 bg-kedua border border-utama rounded-full text-utama'
	};

	$: visibilityBadgeConfig = {
		text: 'Public',
		classes: 'px-4 py-2 bg-utama text-black border border-utama rounded-full'
	};

	// AgentStatus reactive uptime calculation
	$: agentStatus = selectedAgent?.status || 'running';
	$: startedAtTime = dashboardData?.startedAt || '--';
	$: calculatedUptime = calculateUptime(startedAtTime, currentTime, agentStatus);

	// Component data reactivity
	$: statsData = {
		totalIntents: dashboardData?.totalIntents || '0',
		successRate: dashboardData?.successRate || '0',
		avgResponse: dashboardData?.avgResponse || '0',
		activeUsers: dashboardData?.activeUsers || '0'
	};

	$: resourceUtilizationData = {
		resourceUtilization: dashboardData?.resourceUtilization || 0,
		showStatus: true,
		thresholds: { low: 40, medium: 70, high: 90 }
	};

	$: rightSidebarData = {
		agentStatus: 'running',
		status: 'running',
		uptime: calculatedUptime,
		memoryUsage: agentStatus === 'stopped' ? '0 MB' : dashboardData?.memoryUsage || '-- MB',
		cpuUsage: agentStatus === 'stopped' ? '0%' : dashboardData?.cpuUsage || '--%',
		startedAt: startedAtTime,
		recentActivity: dashboardData?.recentActivity || [],
		agentDetails: {
			created: dashboardData?.agentDetails?.created || '--/--/----',
			lastUpdated: dashboardData?.agentDetails?.lastUpdated || '--/--/----',
			agentId: '262316b4',
			loggingLevel: dashboardData?.agentDetails?.loggingLevel || 'info',
			autoRestart: dashboardData?.agentDetails?.autoRestart !== undefined
				? dashboardData.agentDetails.autoRestart
				: true
		}
	};

	$: fileExplorerData = {
		agent,
		error: codeDataError,
		files: filteredFiles,
		selectedFileId: selectedFileId,
		searchQuery: searchQuery
	};

	$: codeEditorData = {
		agent,
		activeFile: activeFile,
		selectedFileId: selectedFileId,
		lastUpdated: displayCodeData.lastUpdated,
		isFullscreen
	};

	$: logsData = {
		logs: logs,
		isLoading: isLoadingLogs,
		isStreaming: isStreaming,
		error: logsError,
		filters,
		agent: { name: 'Monitor Agent', status: 'running' }
	};

	// Available filter options reactivity (now using static arrays)
	// logLevels and logSources are defined as constants above

	// Auto-initialization and state management reactivity
	$: if (displayCodeData.activeFileId && !selectedFileId) {
		selectedFileId = displayCodeData.activeFileId;
	}

	$: if (currentView === 'logs' && isStreaming && !streamingInterval) {
		initializeLogsData();
		startStreaming();
	}
	$: if (currentView !== 'logs' && streamingInterval) {
		stopStreaming();
	}

	$: if (logs.length > 0) {
		updateAvailableOptions();
		filterLogs();
	}

	$: if (agentStatus === 'running') {
		startUptimeTimer();
	} else if (uptimeInterval) {
		clearInterval(uptimeInterval);
		uptimeInterval = null;
	}

	// ========================================
	// 3. DATA INPUT TO DATABASE
	// ========================================

	// Clear logs in backend/database
	async function clearLogsOnBackend() {
		try {
			// TODO: Replace with actual API call to database
			if (typeof window !== 'undefined' && window.agentLogsStore) {
				delete window.agentLogsStore['logs_monitor_agent'];
			}
		} catch (err) {
			console.error('Failed to clear logs:', err);
			logsError = 'Failed to clear logs';
		}
	}

	// Save code changes to database
	function handleCodeEdit(event) {
		// TODO: Save to backend/database
		dispatch('code-edit', { ...event.detail, timestamp: new Date().toISOString() });
	}

	// Fetch new logs from Supabase every 7 seconds
	function startStreaming() {
		if (!autoRefresh) return;

		streamingInterval = setInterval(async () => {
			// Manage log array size to prevent memory issues
			if (logs.length >= maxLogEntries) {
				logs = logs.slice(-Math.floor(maxLogEntries * 0.8));
			}

			// Fetch new logs from Supabase
			await fetchLogsFromSupabase();

			// Update filtered logs
			filterLogs();

			// Auto-scroll if enabled
			if (autoScroll && logContainer) {
				setTimeout(() => {
					logContainer.scrollTop = logContainer.scrollHeight;
				}, 50);
			}
		}, refreshInterval);
	}

	// Clear logs data in database
	function handleClearLogs() {
		logs = [];
		selectedLogId = null;
		lastFetchTime = null;
		pageVisitTime = new Date(); // Reset page visit time
		filterLogs();
		clearLogsOnBackend();
	}

	// Store file selection data to database
	function handleFileSelectCode(fileId) {
		const file = displayCodeData.files.find((f) => f.id === fileId);
		selectedFileId = fileId;
		// TODO: Store file selection to database
		dispatch('file-select', {
			fileId,
			file,
			timestamp: new Date().toISOString()
		});
	}

	// Store search query to database
	function handleSearchInputCode(event) {
		const newQuery = event.target.value;
		searchQuery = newQuery;
		// TODO: Store search history to database
		dispatch('search-query-change', newQuery);
	}

	// Store view changes to database
	async function handleTabChange(event) {
		const { newTabId } = event.detail;
		const previousView = currentView;
		currentView = newTabId;

		if (newTabId === 'code') {
			await loadCodeData();
		}

		// TODO: Store view preferences to database
		dispatch('view-change', { view: newTabId });
	}

	// Store tab selection to database
	function handleTabSelect(tab) {
		if (tab.disabled || navigationData.isLoading) return;

		// TODO: Store tab selection preferences to database
		dispatch('tab-change', {
			previousTabId: navigationData.activeTabId,
			newTabId: tab.id,
			tabData: tab
		});

		navigationData.activeTabId = tab.id;
	}

	// Store filter changes to database
	function handleFilterChange(event) {
		const { filterType, value } = event.detail;
		filters[filterType] = value;
		filterLogs();
		// TODO: Store filter preferences to database
	}

	// Store log selection to database
	function handleLogSelect(event) {
		const { logId } = event.detail;
		selectedLogId = selectedLogId === logId ? null : logId;
		// TODO: Store log selection preferences to database
	}

	// Store auto-scroll preference to database
	function handleAutoScrollToggle() {
		autoScroll = !autoScroll;
		// TODO: Store auto-scroll preference to database
	}

	// Store timestamps preference to database
	function handleTimestampsToggle() {
		showTimestamps = !showTimestamps;
		// TODO: Store timestamps preference to database
	}

	// Store streaming preference to database
	function handleStreamingToggle(event) {
		if (event.detail && typeof event.detail.isStreaming === 'boolean') {
			isStreaming = event.detail.isStreaming;
		} else {
			isStreaming = !isStreaming;
		}

		if (isStreaming) {
			startStreaming();
		} else {
			stopStreaming();
		}

		// TODO: Store streaming preference to database
	}

	// ===== UTILITY FUNCTIONS (Non-categorized helpers) =====

	function formatFileSize(content) {
		const bytes = new Blob([content]).size;
		if (bytes < 1024) return `${bytes} B`;
		if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
		return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
	}

	function getSyntaxClass(type) {
		return `language-${type}`;
	}

	function updateAvailableOptions() {
		// This function exists for compatibility but filter options are now static
	}

	function filterLogs() {
		filteredLogs = logs.filter((log) => {
			const levelMatch =
				filters.level === 'all' || log.level.toLowerCase() === filters.level.toLowerCase();
			const sourceMatch = filters.source === 'all' || log.source === filters.source;
			const searchMatch =
				filters.searchQuery === '' ||
				log.message.toLowerCase().includes(filters.searchQuery.toLowerCase()) ||
				log.level.toLowerCase().includes(filters.searchQuery.toLowerCase()) ||
				log.source.toLowerCase().includes(filters.searchQuery.toLowerCase());

			return levelMatch && sourceMatch && searchMatch;
		});
	}

	function calculateUptime(startedAtString, currentTime, status) {
		if (!startedAtString || startedAtString === '--' || status === 'stopped') {
			return '--:--:--';
		}

		try {
			const [datePart, timePart] = startedAtString.split(', ');
			const [day, month, year] = datePart.split('/');
			const [hours, minutes, seconds] = timePart.split(':');

			const startedAt = new Date(
				parseInt(year),
				parseInt(month) - 1,
				parseInt(day),
				parseInt(hours),
				parseInt(minutes),
				parseInt(seconds)
			);

			const diffMs = currentTime.getTime() - startedAt.getTime();

			if (diffMs < 0) {
				return '--:--:--';
			}

			const totalSeconds = Math.floor(diffMs / 1000);
			const uptimeHours = Math.floor(totalSeconds / 3600);
			const uptimeMinutes = Math.floor((totalSeconds % 3600) / 60);
			const uptimeSeconds = totalSeconds % 60;

			return `${uptimeHours.toString().padStart(2, '0')}:${uptimeMinutes.toString().padStart(2, '0')}:${uptimeSeconds.toString().padStart(2, '0')}`;
		} catch (error) {
			console.error('Error calculating uptime:', error);
			return '--:--:--';
		}
	}

	function startUptimeTimer() {
		if (uptimeInterval) clearInterval(uptimeInterval);

		uptimeInterval = setInterval(() => {
			currentTime = new Date();
		}, 1000);
	}

	function getUtilizationStatus(utilization) {
		const thresholds = resourceUtilizationData.thresholds || { low: 40, medium: 70, high: 90 };
		if (utilization >= thresholds.high) return 'high';
		if (utilization >= thresholds.medium) return 'medium';
		return 'low';
	}

	function getStatusStyle(status) {
		const styles = {
			low: 'bg-kedua text-utama',
			medium: 'bg-[#221A00] text-[#FFA600]',
			high: 'bg-[#220007] text-[#F80036]',
			loading: 'bg-gray-900 text-gray-300'
		};
		return styles[status] || styles.loading;
	}

	function getStatusText(status) {
		const texts = {
			low: 'Low',
			medium: 'Medium',
			high: 'High',
			loading: 'Loading...'
		};
		return texts[status] || 'Unknown';
	}

	function getTabClasses(tab, isActive, disabled) {
		const baseClasses = 'relative w-[150px] px-4 py-2 transition-all duration-200';

		if (disabled || tab.disabled) {
			return `${baseClasses} cursor-not-allowed opacity-50 text-abu`;
		}

		if (isActive) {
			return `${baseClasses} text-utama bg-kedua border border-utama rounded-full`;
		}

		return `${baseClasses} text-[#ECF2FF] hover:text-[#ECF2FF] border border-transparent rounded-full`;
	}

	function getLogLevelClass(level) {
		switch (level.toLowerCase()) {
			case 'info':
				return 'text-utama';
			case 'warn':
				return 'text-[#FFA600]';
			case 'error':
				return 'text-[#F80036]';
			case 'debug':
				return 'text-[#42AAFF]';
			default:
				return 'text-[#ECF2FF]';
		}
	}

	function getBorderLevelClass(level) {
		switch (level.toLowerCase()) {
			case 'info':
				return 'border-l-utama';
			case 'warn':
				return 'border-l-[#FFA600]';
			case 'error':
				return 'border-l-[#F80036]';
			case 'debug':
				return 'border-l-[#42AAFF]';
			default:
				return 'border-l-white';
		}
	}

	function stopStreaming() {
		if (streamingInterval) {
			clearInterval(streamingInterval);
			streamingInterval = null;
		}
	}

	function pauseLogsStreaming() {
		if (isStreaming) {
			isStreaming = false;
			stopStreaming();
		}
	}

	function resumeLogsStreaming() {
		if (!isStreaming) {
			isStreaming = true;
			if (autoRefresh) {
				startStreaming();
			}
		}
	}

	function handleSwitchToLogs() {
		currentView = 'logs';
	}

	function handleDownloadCode() {
		const activeFileForDownload = displayCodeData.files.find((f) => f.id === selectedFileId);
		if (activeFileForDownload) {
			const blob = new Blob([activeFileForDownload.content], { type: 'text/plain' });
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = `agent_${activeFileForDownload.name}`;
			a.click();
			URL.revokeObjectURL(url);
		}
		dispatch('file-download', {
			fileId: selectedFileId,
			fileName: activeFile?.name
		});
	}

	function toggleFullscreenCode() {
		isFullscreen = !isFullscreen;
		dispatch('fullscreen-toggle', {
			isFullscreen: isFullscreen,
			fileId: selectedFileId
		});
	}

	async function handleCopyCode() {
		if (activeFile) {
			try {
				await navigator.clipboard.writeText(activeFile.content);
				isCopied = true;
				dispatch('code-copy', {
					fileId: selectedFileId,
					fileName: activeFile.name,
					contentLength: activeFile.content.length
				});
				setTimeout(() => {
					isCopied = false;
				}, 2000);
			} catch (err) {
				console.error('Failed to copy text: ', err);
			}
		}
	}

	function handleDownloadLogs(event) {
		const timestamp = new Date().toISOString().split('T')[0];
		const logsText = filteredLogs
			.map(
				(log) =>
					`[${log.timestamp}] ${log.level}: ${log.message}${
						log.details ? ' | ' + JSON.stringify(log.details) : ''
					}`
			)
			.join('\n');

		const blob = new Blob([logsText], { type: 'text/plain' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `monitor-agent-logs-${timestamp}.txt`;
		a.click();
		URL.revokeObjectURL(url);
	}

	function handleTabKeydown(event, tab) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			handleTabSelect(tab);
		}
	}

	function handleFileSelect(event) {
		selectedFileId = event.detail.fileId;
		dispatch('file-select', { ...event.detail, timestamp: new Date().toISOString() });
	}

	function handleCodeCopy(event) {
		dispatch('code-copy', event.detail);
	}

	function handleFileDownload(event) {
		const activeFileForDownload = displayCodeData.files.find((f) => f.id === event.detail.fileId);
		if (activeFileForDownload) {
			const blob = new Blob([activeFileForDownload.content], { type: 'text/plain' });
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = `agent_${activeFileForDownload.name}`;
			a.click();
			URL.revokeObjectURL(url);
		}
		dispatch('file-download', event.detail);
	}

	function handleFullscreenToggle(event) {
		isFullscreen = event.detail.isFullscreen;
		dispatch('fullscreen-toggle', event.detail);
	}

	function handleSearchQueryChange(event) {
		searchQuery = event.detail;
	}

	// Clean up intervals on component destroy
	onDestroy(() => {
		if (streamingInterval) {
			clearInterval(streamingInterval);
		}
		if (uptimeInterval) {
			clearInterval(uptimeInterval);
		}
		if (dashboardRefreshInterval) {
			clearInterval(dashboardRefreshInterval);
		}
	});

	// Initialize dashboard data from Supabase
	async function initializeDashboardData() {
		const serverStatusData = await fetchServerStatusFromSupabase();
		if (serverStatusData) {
			dashboardStore.set(serverStatusData);
		} else {
			// Fallback to mock data if Supabase fetch fails
			dashboardStore.set(mockDashboardData);
		}
	}

	// Refresh dashboard data periodically
	function startDashboardRefresh() {
		if (dashboardRefreshInterval) {
			clearInterval(dashboardRefreshInterval);
		}

		dashboardRefreshInterval = setInterval(async () => {
			const serverStatusData = await fetchServerStatusFromSupabase();
			if (serverStatusData) {
				dashboardStore.set(serverStatusData);
			}
		}, 10000); // Refresh every 10 seconds
	}

	// Initialize dashboard data on component mount
	initializeDashboardData().then(() => {
		startDashboardRefresh();
	});
</script>

<svelte:head>
	<title>Monitor Agent - {currentView.charAt(0).toUpperCase() + currentView.slice(1)}</title>
	<meta
		name="description"
		content="{currentView.charAt(0).toUpperCase() + currentView.slice(1)} for AI agent"
	/>
</svelte:head>

<Header />

<section
	class="min-h-screen w-full shadow-sm p-8 grid grid-rows-[auto_auto_1fr]"
	out:fade|global={{ duration: 300 }}
>
	<PageTitle subtitle="My Agents" title="Monitor Agent" {address} />

	<AnalyticsNavigation
		{navigationData}
		{statusBadgeConfig}
		{visibilityBadgeConfig}
		{getTabClasses}
		on:tab-change={handleTabChange}
	/>

	<div class="flex overflow-hidden">
		{#if currentView === 'analytics'}
			<div class="flex-1 flex flex-col pr-4 overflow-auto">
				<StatsGrid data={statsData} {agent} />
				<ChartsGrid
					intentVolumeData={dashboardData?.intentVolume || []}
					intentCategoriesData={dashboardData?.intentCategories || []}
					{agent}
				/>
				<BottomGrid
					{resourceUtilizationData}
					{getUtilizationStatus}
					{getStatusStyle}
					{getStatusText}
					responseTimeData={dashboardData?.responseTimeDistribution || []}
					{agent}
				/>
			</div>
			<RightSidebar
				data={rightSidebarData}
				{agent}
				{statusConfig}
				{calculateUptime}
				{currentTime}
				{agentStatus}
				on:switch-to-logs={handleSwitchToLogs}
			/>
		{:else if currentView === 'code'}
			<div class="flex-1 overflow-hidden">
				<CodePage
					{fileExplorerData}
					{codeEditorData}
					{isFullscreen}
					{formatFileSize}
					{getSyntaxClass}
					{isCopied}
					handleFileSelect={handleFileSelectCode}
					handleDownload={handleDownloadCode}
					handleSearchInput={handleSearchInputCode}
					toggleFullscreen={toggleFullscreenCode}
					handleCopy={handleCopyCode}
					on:file-select={handleFileSelect}
					on:code-edit={handleCodeEdit}
					on:code-copy={handleCodeCopy}
					on:file-download={handleFileDownload}
					on:fullscreen-toggle={handleFullscreenToggle}
					on:search-query-change={handleSearchQueryChange}
				/>
			</div>
		{:else if currentView === 'logs'}
			<div class="flex-1 overflow-hidden">
				<LogsPage
					{logsData}
					{filteredLogs}
					{selectedLogId}
					{autoScroll}
					{showTimestamps}
					isStreaming={logsData.isStreaming}
					{logLevels}
					{logSources}
					{getLogLevelClass}
					{getBorderLevelClass}
					bind:logContainer
					{initializeLogsData}
					{fetchLogs}
					{pauseLogsStreaming}
					{resumeLogsStreaming}
					on:clear-logs={handleClearLogs}
					on:download-logs={handleDownloadLogs}
					on:filter-change={handleFilterChange}
					on:log-select={handleLogSelect}
					on:auto-scroll-toggle={handleAutoScrollToggle}
					on:timestamps-toggle={handleTimestampsToggle}
					on:streaming-toggle={handleStreamingToggle}
				/>
			</div>
		{/if}
	</div>
</section>
