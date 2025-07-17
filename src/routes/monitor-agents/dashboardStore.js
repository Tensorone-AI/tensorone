import { writable } from 'svelte/store';
import { mockDashboardData } from './mockData.js';

export const dashboardStore = writable(mockDashboardData);

// Add only the selected agent store for status reactivity
export const selectedAgentStore = writable(null);

// Helper function to update only the status of the selected agent
export function updateSelectedAgentStatus(newStatus) {
	selectedAgentStore.update((agent) => {
		if (agent) {
			const updatedAgent = { ...agent, status: newStatus };
			console.log('Updating selected agent status:', newStatus, updatedAgent);
			return updatedAgent;
		}
		return agent;
	});
}

// Helper function to get current selected agent
export function getSelectedAgent() {
	let agent = null;
	selectedAgentStore.subscribe((value) => {
		agent = value;
	})();
	return agent;
}

// Helper function to set the selected agent with proper logging
export function setSelectedAgent(agent) {
	console.log('Setting selected agent:', agent);
	selectedAgentStore.set(agent);
}

// API service functions for backend integration
export const dashboardApi = {
	async fetchDashboardData() {
		try {
			const response = await fetch('/api/dashboard');
			const data = await response.json();
			dashboardStore.set(data);
			return data;
		} catch (error) {
			console.error('Failed to fetch dashboard data:', error);
			throw error;
		}
	},

	async fetchStats() {
		try {
			const response = await fetch('/api/dashboard/stats');
			return await response.json();
		} catch (error) {
			console.error('Failed to fetch stats:', error);
			throw error;
		}
	},

	async fetchAgentDetails() {
		try {
			const response = await fetch('/api/dashboard/agent-details');
			return await response.json();
		} catch (error) {
			console.error('Failed to fetch agent details:', error);
			throw error;
		}
	},

	async fetchIntentVolume(days = 7) {
		try {
			const response = await fetch(`/api/dashboard/intent-volume?days=${days}`);
			return await response.json();
		} catch (error) {
			console.error('Failed to fetch intent volume:', error);
			throw error;
		}
	},

	async fetchRecentActivity(limit = 10) {
		try {
			const response = await fetch(`/api/dashboard/activity?limit=${limit}`);
			return await response.json();
		} catch (error) {
			console.error('Failed to fetch recent activity:', error);
			throw error;
		}
	}
};
