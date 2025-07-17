<script>
	// Icon imports
	import barchartIcon from '$lib/img/bar-chart-icon.svg';
	import trendingupIcon from '$lib/img/trending-up-icon.svg';
	import clockIcon from '$lib/img/clock-icon.svg';
	import usersIcon from '$lib/img/users-icon.svg';

	export let title = '';
	export let value = '';
	export let icon = 'chart';

	const icons = {
		chart: barchartIcon,
		'trending-up': trendingupIcon,
		clock: clockIcon,
		users: usersIcon
	};
</script>

<div class="card card-compact bg-[#0C0D12] rounded-xl w-full relative overflow-hidden p-6">
	<div class="flex items-center justify-between mb-2">
		<span class="text-[#ECF2FF]">{title}</span>
		<img src={icons[icon]} alt="Icon" />
	</div>
	<div class="text-3xl text-utama font-medium">{value}</div>
</div>
