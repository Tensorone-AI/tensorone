<script>
	// ================================
	// IMPORTS & EXPORTS
	// ================================
	import Header from '../Header.svelte';
	import PageTitle from '../PageTitle.svelte';
	import { fade, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { onMount, afterUpdate } from 'svelte';
	import ChatHeader from './ChatHeader.svelte';
	import DateSeparator from './DateSeparator.svelte';
	import MessagesContainer from './MessagesContainer.svelte';
	import ChatInput from './ChatInput.svelte';
	import HistorySidebar from './HistorySidebar.svelte';
	import DeleteModal from './DeleteModal.svelte';
	import ShareModal from './ShareModal.svelte';
	import { wallet } from '$lib/stores/wallet';
	import { encryptShareableID } from '$lib/utils/encryption';

	// Props
	export let data = {};

	// ================================
	// STATE MANAGEMENT
	// ================================

	// Core reactive state variables
	let isLoading = false;
	let messagesContainer;
	let shouldAutoScroll = true;
	let isSidebarOpen = true;
	let prompt = '';
	let newChat = true;
	let chatTitle = 'New Chat';
	let currentConversationId = '';
	let currentDateTime = '';
	let conversations = new Map(); // Store conversations by ID
	let chatHistory = []; // List of chat sessions

	// Modal states
	let itemToDelete = null;
	let isOpenDeleteModal = false;
	let isOpenShareModal = false;

	// Copy message state
	let copyStates = {};

	// Reactive assignments
	$: address = data?.address || $wallet?.address || '';
	$: conversation = conversations.get(currentConversationId) || [];
	$: chatItems = chatHistory.map((item) => ({
		id: item.id,
		title: item.title,
		isActive: item.id === currentConversationId,
		shareableID: encryptShareableID(item.shareableID || item.id)
	}));
	$: shareableID = currentConversationId ? encryptShareableID(currentConversationId) : '';
	$: activeConversationDate =
		chatHistory.find((item) => item.id === currentConversationId)?.date || currentDateTime;

	// ================================
	// LIFECYCLE FUNCTIONS
	// ================================

	onMount(async () => {
		const date = new Date();
		currentDateTime = formatDateTime(date);
		await loadChatTitles();
		initializeNewChat();
	});

	afterUpdate(() => {
		if (shouldAutoScroll && messagesContainer) {
			scrollToBottom();
		}
	});

	// ================================
	// UTILITY FUNCTIONS
	// ================================

	function formatDateTime(date) {
		const options = {
			day: 'numeric',
			month: 'long',
			year: 'numeric'
		};
		return date.toLocaleDateString('en-GB', options);
	}

	function scrollToBottom() {
		if (messagesContainer) {
			messagesContainer.scrollTop = messagesContainer.scrollHeight;
		}
	}

	function handleScroll() {
		if (messagesContainer) {
			const { scrollTop, scrollHeight, clientHeight } = messagesContainer;
			shouldAutoScroll = scrollTop + clientHeight >= scrollHeight - 100;
		}
	}

	// ================================
	// CHAT MANAGEMENT
	// ================================

	async function loadChatTitles() {
		if (!address) return;

		try {
			const response = await fetch(
				`/api/playground/chat/list-title?address=${encodeURIComponent(address)}`,
				{
					method: 'GET',
					headers: {
						'Content-Type': 'application/json'
					}
				}
			);

			if (response.ok) {
				const data = await response.json();
				if (data.titles && Array.isArray(data.titles)) {
					chatHistory = data.titles.map((item) => ({
						id: item.id,
						title: item.title,
						date: formatDateTime(new Date(item.created_at)),
						shareableID: item.id
					}));
				}
			}
		} catch (error) {
			console.error('Failed to load chat titles:', error);
		}
	}

	async function generateChatTitle(userMessage) {
		if (!address) return;

		try {
			const response = await fetch('/api/playground/chat/generate-title', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					text: userMessage,
					address: address
				})
			});

			if (response.ok) {
				const data = await response.json();
				if (data.title && data.id) {
					chatTitle = data.title;
					currentConversationId = data.id;
					newChat = false;

					// Reload chat titles to get the updated list
					await loadChatTitles();
				}
			}
		} catch (error) {
			console.error('Failed to generate chat title:', error);
		}
	}

	function initializeNewChat() {
		currentConversationId = crypto.randomUUID();
		newChat = true;
		chatTitle = 'New Chat';
		conversations.set(currentConversationId, []);
		conversations = conversations; // Trigger reactivity
	}

	function handleNewChat() {
		initializeNewChat();
	}

	async function loadConversation(conversationId) {
		try {
			console.log('Loading conversation:', conversationId);
			const response = await fetch('/api/playground/chat/retrieve-chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					id: conversationId
				})
			});

			console.log('Response:', response);

			if (response.ok) {
				const data = await response.json();
				if (data.messages) {
					const formattedMessages = data.messages.map((msg) => ({
						type: msg.role === 'user' ? 'user' : 'assistant',
						message: msg.content
					}));
					conversations.set(conversationId, formattedMessages);
					conversations = conversations; // Trigger reactivity
				}
			}
		} catch (error) {
			console.error('Failed to load conversation:', error);
		}
	}

	function toggleActiveHistory(id) {
		currentConversationId = id;
		newChat = false;

		const chatItem = chatHistory.find((item) => item.id === id);
		if (chatItem) {
			chatTitle = chatItem.title;
			// Load conversation if not already loaded
			if (!conversations.has(id)) {
				loadConversation(id);
			}
		}
	}

	// ================================
	// CHAT FUNCTIONALITY
	// ================================

	async function sendMessage() {
		if (!prompt.trim() || isLoading) return;

		isLoading = true;
		shouldAutoScroll = true;
		const userMessage = prompt.trim();
		prompt = '';

		// Add user message to conversation
		const currentConv = conversations.get(currentConversationId) || [];
		const updatedConv = [...currentConv, { type: 'user', message: userMessage }];
		conversations.set(currentConversationId, updatedConv);
		conversations = conversations; // Trigger reactivity

		try {
			// If this is a new chat, generate title first
			if (newChat) {
				await generateChatTitle(userMessage);
			}

			const response = await fetch('/api/playground/chat/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					id: currentConversationId,
					message: userMessage
				})
			});

			if (!response.ok) {
				throw new Error('Failed to send message');
			}

			const data = await response.json();

			if (data.messages) {
				// Convert backend format to frontend format
				const formattedMessages = data.messages.map((msg) => ({
					type: msg.role === 'user' ? 'user' : 'assistant',
					message: msg.content
				}));

				conversations.set(currentConversationId, formattedMessages);
				conversations = conversations; // Trigger reactivity
			}
		} catch (error) {
			console.error('Chat error:', error);
			// Add error message to conversation
			const errorConv = conversations.get(currentConversationId) || [];
			conversations.set(currentConversationId, [
				...errorConv,
				{
					type: 'assistant',
					message: 'Sorry, I encountered an error. Please try again.'
				}
			]);
			conversations = conversations; // Trigger reactivity
		} finally {
			isLoading = false;
		}
	}

	// ================================
	// INPUT HANDLING
	// ================================

	function updatePrompt(event) {
		prompt = event.target.value;
	}

	function handleKeydown(event) {
		if (event.key === 'Enter') {
			if (!event.shiftKey) {
				event.preventDefault();
				sendMessage();
			}
		}
	}

	// ================================
	// SIDEBAR FUNCTIONS
	// ================================

	function toggleSidebar() {
		isSidebarOpen = !isSidebarOpen;
	}

	// ================================
	// MODAL FUNCTIONS
	// ================================

	function toggleDeleteModal(item) {
		itemToDelete = item;
		isOpenDeleteModal = !isOpenDeleteModal;
	}

	function closeDeleteModal() {
		isOpenDeleteModal = false;
		itemToDelete = null;
	}

	function toggleShareModal() {
		isOpenShareModal = !isOpenShareModal;
	}

	function closeShareModal() {
		isOpenShareModal = false;
	}

	async function deleteChat() {
		if (itemToDelete) {
			try {
				const response = await fetch('/api/playground/chat/delete-title', {
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						id: itemToDelete.id
					})
				});

				if (response.ok) {
					// Remove from local state
					conversations.delete(itemToDelete.id);
					conversations = conversations; // Trigger reactivity

					// If deleted chat was active, start new chat
					if (currentConversationId === itemToDelete.id) {
						handleNewChat();
					}

					// Reload chat titles for better reactivity
					await loadChatTitles();
				}
			} catch (error) {
				console.error('Failed to delete chat:', error);
			}
		}

		closeDeleteModal();
	}

	// ================================
	// SHARE FUNCTIONS
	// ================================

	function copyLink() {
		console.log('copyLink - shareableID:', shareableID);
		console.log('copyLink - currentConversationId:', currentConversationId);
		navigator.clipboard.writeText(
			`https://shareable.tensorone.ai/${encodeURIComponent(shareableID)}`
		);
	}

	async function handleCopyMessage(message, messageId) {
		try {
			await navigator.clipboard.writeText(message);
			copyStates[messageId] = 'success';
			copyStates = copyStates; // Trigger reactivity
			setTimeout(() => {
				copyStates[messageId] = 'default';
				copyStates = copyStates; // Trigger reactivity
			}, 2000);
		} catch (err) {
			copyStates[messageId] = 'error';
			copyStates = copyStates; // Trigger reactivity
			setTimeout(() => {
				copyStates[messageId] = 'default';
				copyStates = copyStates; // Trigger reactivity
			}, 2000);
		}
	}
</script>

<svelte:head>
	<title>Uncensored AI Chat</title>
	<meta
		name="description"
		content="Engage in unrestricted conversations with Tensorone's Uncensored AI Chat. Experience open-ended interactions in our innovative playground section."
	/>
</svelte:head>

<Header />

<div class="min-h-screen w-full overflow-hidden px-4">
	<div
		in:fly={{
			delay: 100,
			duration: 800,
			y: 50,
			opacity: 0,
			easing: quintOut
		}}
		out:fade={{ duration: 200 }}
	>
		<div class="relative w-full">
			<div class="p-4 h-screen">
				<section
					class="col-span-12 w-full shadow-sm relative"
					in:fly={{
						delay: 200,
						duration: 600,
						y: -30,
						opacity: 0,
						easing: quintOut
					}}
					out:fade={{ duration: 200 }}
				>
					<div in:fade={{ delay: 300, duration: 400 }} out:fade={{ duration: 200 }}>
						<PageTitle subtitle={'Playground'} title="Uncensored AI Chat" {address} />

						<div
							class="relative bg-black border border-[#444A61] rounded-xl h-[calc(100vh-11rem)] flex"
							in:fade|global={{ delay: 300, duration: 500 }}
							out:fade|global={{ duration: 300 }}
						>
							<div
								class={`relative w-full h-[calc(100vh-11rem)] transition-all duration-300 ease-in-out ${isSidebarOpen ? 'lg:w-4/5' : 'lg:w-full'}`}
							>
								<ChatHeader
									{chatTitle}
									{shareableID}
									onNewChat={handleNewChat}
									onToggleShareModal={toggleShareModal}
								/>

								<DateSeparator date={activeConversationDate} />

								<MessagesContainer
									{conversation}
									{isLoading}
									{messagesContainer}
									{copyStates}
									{currentConversationId}
									onScroll={handleScroll}
									onCopyMessage={handleCopyMessage}
									bind:container={messagesContainer}
								/>

								<ChatInput
									{prompt}
									{isLoading}
									onInput={updatePrompt}
									onKeydown={handleKeydown}
									onSubmit={sendMessage}
								/>
							</div>

							<HistorySidebar
								{chatItems}
								{isSidebarOpen}
								onToggleActiveHistory={toggleActiveHistory}
								onToggleDeleteModal={toggleDeleteModal}
								onToggleSidebar={toggleSidebar}
							/>
						</div>
					</div>
				</section>
			</div>
		</div>
	</div>
</div>

<DeleteModal
	isOpen={isOpenDeleteModal}
	{itemToDelete}
	onDelete={deleteChat}
	onClose={closeDeleteModal}
/>

<ShareModal
	isOpen={isOpenShareModal}
	{shareableID}
	onClose={closeShareModal}
	onCopyLink={copyLink}
/>
