export const mockDashboardData = {
	totalIntents: 258,
	successRate: 95,
	avgResponse: 440,
	activeUsers: 5,
	memoryUsage: '128 MB',
	cpuUsage: '2.4%',
	startedAt: '02/06/2025, 23:41:21',
	resourceUtilization: 32,
	intentVolume: [65, 45, 78, 32, 52, 68, 85],
	intentCategories: [
		{ name: 'Data Analysis', percentage: 27 },
		{ name: 'Content Generation', percentage: 11 },
		{ name: 'Task Scheduling', percentage: 24 },
		{ name: 'User Queries', percentage: 26 },
		{ name: 'Other', percentage: 12 }
	],
	responseTimeDistribution: [
		{ range: '0-100ms', count: 45 },
		{ range: '100-200ms', count: 85 },
		{ range: '200-300ms', count: 65 },
		{ range: '300-400ms', count: 58 },
		{ range: '400ms+', count: 25 }
	],
	recentActivity: [
		{
			type: 'Intent Received',
			time: '2 min ago',
			description: 'Received intent "Data Analysis" from user 7XB3...9F4D'
		},
		{
			type: 'Intent Received',
			time: '2 min ago',
			description: 'Received intent "Data Analysis" from user 7XB3...9F4D'
		},
		{
			type: 'Intent Processed',
			time: '5 min ago',
			description: 'Successfully processed intent "Market Analysis" from user 3E4F...7A8B'
		}
	],
	agentDetails: {
		created: '22/05/2026',
		lastUpdated: '22/05/2025',
		agentId: '262316b4',
		loggingLevel: 'Info',
		autoRestart: true
	}
};
