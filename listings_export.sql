--
-- PostgreSQL database dump
--

\restrict 92Bl1TChd3uwqaffCFMazS2Q58qETTQGFUCp3INCbNyEjcZS6QgyDXM3krN3FhZ

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: listings_history; Type: TABLE DATA; Schema: silver; Owner: postgres
--

COPY silver.listings_history (id, listing_hash, title, price, price_per_sqft, area_sqft, locality, city, bhk, source, url, effective_from, effective_to, is_current, record_hash, ingested_at, created_at) FROM stdin;
1	14ff134366b9a4b94519b43242248185	2 BHK Flat in Tumkur Road, Bangalore	12512703	\N	\N	Prestige Jindal City	bangalore	2	99acres	https://www.99acres.com/2-bhk-bedroom-apartment-flat-for-sale-in-prestige-jindal-city-tumkur-road-bangalore-west-984-sq-ft-spid-B90032020	2026-04-21	\N	t	8433b7353bcf097baf8324671e6fd259	2026-04-20 16:27:39.215246	2026-04-21 12:20:31.191378
2	b7e22ccb9b8f9631a69ab206aa15be38	\N	20900000	\N	1665	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	756046205bfb24a2567c6e45e2772e32	2026-04-20 16:27:19.449545	2026-04-21 12:20:31.191378
3	29ce0be4f2a9bd95a854f585665e8c6d	\N	36100000	\N	2407	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	2f68a558496cd063ce208ebed07040f1	2026-04-20 16:27:19.61785	2026-04-21 12:20:31.191378
4	051e959d48e40f0ab7380626facf4bac	\N	32000000	\N	2299	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	e851c23f6b3abf16dab376b53f38a88a	2026-04-20 16:27:19.800183	2026-04-21 12:20:31.191378
5	af11d4bc77b23dd19d821623d3266722	\N	45000000	\N	2500	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	21dc38aada2c0656c868b7d5389d6b92	2026-04-20 16:27:19.921315	2026-04-21 12:20:31.191378
6	883bcf1044a1b3666362840bb7a7d7bb	\N	13200000	\N	1694	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	8191745c883c5568a0194fa2c6df3a63	2026-04-20 16:27:20.039739	2026-04-21 12:20:31.191378
7	d5ea1aa17a5b1ff38d4c9a000c579705	\N	9720000	\N	1281	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	635ad0bbab9c53b6e3932fe93d09e314	2026-04-20 16:27:20.36601	2026-04-21 12:20:31.191378
8	e89216b71d72a73324918e767986922a	\N	43400000	\N	2686	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	bd737e4c713ffeb670ed612c17abaf4a	2026-04-20 16:27:20.530832	2026-04-21 12:20:31.191378
9	efbe9f52aba6cd0c44b86746fe7b9900	\N	38200000	\N	2366	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	1397aa469e42022f4b96d2a4ab54a624	2026-04-20 16:27:20.699813	2026-04-21 12:20:31.191378
10	44f3a65c4c974403737271ed099869ce	\N	28300000	\N	2080	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	e25c86a83e1230758dc1ab7455fb3780	2026-04-20 16:27:20.865667	2026-04-21 12:20:31.191378
11	f9628d8d5a15e9a45879b9cec87eaec2	\N	47900000	\N	2150	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	40f540206353218904e6b227e6af6b17	2026-04-20 16:27:20.982033	2026-04-21 12:20:31.191378
12	8773b78d5c24cba487e81700d5353df1	\N	33700000	\N	2724	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	79f04621e05f8c118ed4023ad95eec5b	2026-04-20 16:27:21.150378	2026-04-21 12:20:31.191378
13	bf19d765213b3d88a636ebef8390ee61	\N	21500000	\N	1944	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	f13873baa9b889c2aaf12828b7190a7c	2026-04-20 16:27:21.316679	2026-04-21 12:20:31.191378
14	b09d2ac2a0ae445d9dc65b275246df57	\N	26000000	\N	2000	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	67e36485dc3d7b274deaa0bad66056fa	2026-04-20 16:27:21.484023	2026-04-21 12:20:31.191378
15	e579cdd85d88064da5dceaef1db5bdaf	\N	11300000	\N	1550	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	2ffbe2b9032447dc858f186f3f2d4707	2026-04-20 16:27:21.649406	2026-04-21 12:20:31.191378
16	c42a4d6fbadc92aa6fc5227432f4d22a	\N	27100000	\N	2244	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	7dc108d0c40dd4fa23cfafabebf2a505	2026-04-20 16:27:21.937572	2026-04-21 12:20:31.191378
17	753d0ba6f74db4afe3c78cb2a487122c	\N	18800000	\N	1803	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	111329a74de83fdcbaccc9020d8c4503	2026-04-20 16:27:22.011963	2026-04-21 12:20:31.191378
18	1ad0d42ee96eed4fcc8330bc77f58253	\N	24400000	\N	1253	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	9ad2e51239201814b61bcc2c1949a5f5	2026-04-20 16:27:22.078312	2026-04-21 12:20:31.191378
19	0f439f16bcbeac98fbe839026e9a8889	\N	39800000	\N	2813	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	783c2b14f0f7ed33d92de01c6af48967	2026-04-20 16:27:22.155167	2026-04-21 12:20:31.191378
20	3d2cf2cdf098b0231daba8f60305593f	\N	18100000	\N	1601	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	e1b2cd83a41c23861f5bc500dfdd2b2f	2026-04-21 12:10:31.39649	2026-04-21 12:20:31.191378
21	5f956f0bf211d97563204de83325f0ae	\N	35300000	\N	NaN	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	ad75e88e12c5cee1578ffb7adea15355	2026-04-21 12:10:31.618045	2026-04-21 12:20:31.191378
22	4a331fe0b885dfc688365ad94b12d6fd	\N	41200000	\N	2140	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	c8895ef750ad30398b2a30eeb40922a7	2026-04-21 12:10:31.744632	2026-04-21 12:20:31.191378
23	d82386de31432dc443f9646023687ddf	\N	20500000	\N	1104	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	af1e24d41407d98d9430f25e2fa01e46	2026-04-21 12:10:31.927754	2026-04-21 12:20:31.191378
24	8d89ddb852ed4c7a143310cd0af7ce16	\N	28000000	\N	1915	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	720f97e8155e39607a4b11a6eac69cc3	2026-04-21 12:10:32.037339	2026-04-21 12:20:31.191378
25	3367a8968f5b1f05c01c63e23522d530	\N	35500000	\N	958	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	21f7a8d60d08acfa374ead841acb184d	2026-04-21 12:10:32.160945	2026-04-21 12:20:31.191378
26	e53f3de576ae941e0e97002fb40be58e	\N	28900000	\N	1759	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	592bdbbd3e53d30d99888115c61dff8c	2026-04-21 12:10:32.297691	2026-04-21 12:20:31.191378
27	c253604baec62a55ca08162bc3c141b2	\N	26700000	\N	1896	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	e94eff53bcfbabfeaa7a8ee6be97db34	2026-04-21 12:10:32.419825	2026-04-21 12:20:31.191378
28	59ae0d7b1d934cb75dfa0ac8c837ca67	\N	19100000	\N	1859	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	a57cc65610cbbfb56471f81cd41d1c13	2026-04-21 12:10:32.541521	2026-04-21 12:20:31.191378
29	1c0545be09c7394bac28a400164e376e	\N	44600000	\N	2000	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	12cd77b1bbc45a9416d9f4e8ee5ff45d	2026-04-21 12:10:32.796911	2026-04-21 12:20:31.191378
30	09441e26a8ff3f899aa4f40ef7b72af7	\N	34500000	\N	2546	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	2e7791739050f907baf88c3dfbfdb1e8	2026-04-21 12:10:32.914969	2026-04-21 12:20:31.191378
31	39c12757bf420f4f0e3012e501caad4f	\N	25400000	\N	1990	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	982cf5ed809cb1ec1d1eb29580c8741e	2026-04-21 12:10:33.019724	2026-04-21 12:20:31.191378
32	e1ceea4a1762a993f848ddd0028424f9	\N	10200000	\N	1506	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	10a20f3222280bd0f60b9a7ca41898ab	2026-04-21 12:10:33.247007	2026-04-21 12:20:31.191378
33	3a7d52c9ada1774d332604b730fb6ac3	\N	17400000	\N	1380	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	edb34c17a01a21fa8ac0171b197f29d6	2026-04-21 12:10:33.369541	2026-04-21 12:20:31.191378
34	c5f086de2c9ac709fab1a06906a669ea	\N	43200000	\N	2954	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	6f7e7f794e70eba5d2f3d47e3defd358	2026-04-21 12:10:33.486079	2026-04-21 12:20:31.191378
35	0613a7742b1ef2cfc1852fc6ef2a644d	\N	13000000	\N	1342	\N	bangalore	\N	magicbricks	\N	2026-04-21	\N	t	a421c2d84d3de6f99e571fde7efb257f	2026-04-21 12:10:33.728176	2026-04-21 12:20:31.191378
36	1e8c6e679fd613477ffa064773ebc684	4 BHK Flat for Sale in Bellandur, Bangalore	40000000	\N	\N	2893 Sq.Ft.	bangalore	4	squareyards	NaN	2026-04-21	\N	t	8bf59bdd90d3509f7fcd3326c4ab3f70	2026-04-20 16:27:57.421814	2026-04-21 12:20:31.191378
37	0a51c9367c4f94300f68b0a8f3877310	3 BHK Flat for Sale in Bellandur, Bangalore	18900000	\N	\N	1650 Sq.Ft.	bangalore	3	squareyards	NaN	2026-04-21	\N	t	1da5f67bcb30c0a15045cf40c6921700	2026-04-20 16:27:57.60151	2026-04-21 12:20:31.191378
38	9b48519b579d86cd3db0d1acdbea11a7	Plot for Sale in Banjara Layout, Bangalore	11400000	\N	\N	Banjara Layout, Bangalore	bangalore	\N	squareyards	NaN	2026-04-21	\N	t	294e5ce32879d01c9dbee073399b1492	2026-04-20 16:27:57.666726	2026-04-21 12:20:31.191378
39	212d2d9c6358dc9d1d39e5e38697b8f0	1 BHK Flat for Sale in Kengeri, Bangalore	4675000	\N	\N	505 Sq.Ft.	bangalore	1	squareyards	NaN	2026-04-21	\N	t	539a4b4fd58dbeb39fc42e282f6a4a57	2026-04-20 16:27:57.741785	2026-04-21 12:20:31.191378
40	55b36e72e88937f7509d46e49c094f8f	2, 3, 4 BHK Flats in\nPuravankara Northern Lights\nBagalur, Bangalore\nStarting From\n₹ 1.19 Cr\n+ Charges	11900000	\N	\N	Starting From\n₹ 1.19 Cr\n+ Charges	bangalore	4	squareyards	https://www.squareyards.com/puravankara-northern-lights-bagalur-bangalore-npd-343636	2026-04-21	\N	t	6282c63dc9831520dc26d062419a9369	2026-04-20 16:27:57.816969	2026-04-21 12:20:31.191378
41	b6ad721da7ea919bb9b8309cb5662524	3 BHK Flat for Sale in Hsr Layout, Bangalore	24000000	\N	\N	Hsr Layout, Bangalore	bangalore	3	squareyards	NaN	2026-04-21	\N	t	d3d6b2aab7054c68e93f0fae6b53aab5	2026-04-20 16:27:57.876123	2026-04-21 12:20:31.191378
42	31fd112e945eca02cd65013fc9f125db	3 BHK Flat for Sale in Thanisandra Main Road, Bangalore	22000000	\N	\N	1576 Sq.Ft.	bangalore	3	squareyards	NaN	2026-04-21	\N	t	eaf9f183ad89b1673e3e959fa591bf2d	2026-04-20 16:27:57.965992	2026-04-21 12:20:31.191378
43	ed54dd1842c9f7f738ab44d058284b68	6+ BHK Builder Floor for Sale in Banashankari 3rd Stage, Bangalore	70000000	\N	\N	Banashankari 3rd Stage, Bangalore	bangalore	\N	squareyards	NaN	2026-04-21	\N	t	74616c180ff0265706372c57cc1d220b	2026-04-20 16:27:58.064427	2026-04-21 12:20:31.191378
44	13076c18ab6daeba0ed4beea818fab0f	Office Space for Sale in Kasturi Nagar, Bangalore	180000000	\N	\N	Kasturi Nagar, Bangalore	bangalore	\N	squareyards	NaN	2026-04-21	\N	t	01ae05e612d19b0dc82045136ad6aee4	2026-04-20 16:27:58.285199	2026-04-21 12:20:31.191378
45	7699f62b984563a3019176903c28b236	3 BHK Flat for Sale in Bidare Agraha, Bangalore	17000000	\N	\N	1563 Sq.Ft.	bangalore	3	squareyards	NaN	2026-04-21	\N	t	67c1f223c529ed4d3d0d816243d9a0b0	2026-04-20 16:27:58.397992	2026-04-21 12:20:31.191378
46	0cb8e732b27f78e71479e9fcc9f19477	2.5 BHK Flat for Sale in Sarjapur, Bangalore	15500000	\N	\N	1254 Sq.Ft.	bangalore	5	squareyards	NaN	2026-04-21	\N	t	69e622c3a0fd341af4344a7be304aa7b	2026-04-20 16:27:58.516932	2026-04-21 12:20:31.191378
47	ccc56d9e85670dd74521662eec6079dd	2.5 BHK Flat for Sale in Yeshwanthpur, Bangalore	16900000	\N	\N	1445 Sq.Ft.	bangalore	5	squareyards	NaN	2026-04-21	\N	t	d96ae4a68c0dc00ad1cac749b68c9e97	2026-04-21 12:11:34.479422	2026-04-21 12:20:31.191378
48	0558d612a4c643e5e2fc72b065c527f9	3 BHK Flat for Sale in Kacharakanahalli, Bangalore	18900000	\N	\N	1844 Sq.Ft.	bangalore	3	squareyards	NaN	2026-04-21	\N	t	1da5f67bcb30c0a15045cf40c6921700	2026-04-21 12:11:34.785417	2026-04-21 12:20:31.191378
49	af9a05a3e525de251a5ec9d388c21251	Plot for Sale in Nri Layout, Bangalore	21000000	\N	\N	Nri Layout, Bangalore	bangalore	\N	squareyards	NaN	2026-04-21	\N	t	c36a74713c85e7f8aa525e7161297f61	2026-04-21 12:11:34.99279	2026-04-21 12:20:31.191378
50	0fce6d6be93c832e4fee3332e316b9fb	1 BHK Flat for Sale in Kengeri, Bangalore	5314000	\N	\N	574 Sq.Ft.	bangalore	1	squareyards	NaN	2026-04-21	\N	t	500b8cedd604eb843ba4f1f437048360	2026-04-21 12:11:35.135832	2026-04-21 12:20:31.191378
51	da7fac1f825deaa51bc0beb479136fcb	3 BHK Flat for Sale in Bannerghatta Road, Bangalore	33000000	\N	\N	1859 Sq.Ft.	bangalore	3	squareyards	NaN	2026-04-21	\N	t	8a0d8b207ca194a1fa9c5c784238df63	2026-04-21 12:11:35.270419	2026-04-21 12:20:31.191378
52	54c668cd77d082f154164924845dadf3	3 BHK Flat for Sale in Kudlu Gate, Bangalore	30000000	\N	\N	1850 Sq.Ft.	bangalore	3	squareyards	NaN	2026-04-21	\N	t	4942d2f03078083532f785b3421c2b45	2026-04-21 12:11:35.536144	2026-04-21 12:20:31.191378
53	09b07736a11ba89cfba43dd60e561682	4 BHK Builder Floor in Janakpuri, West Delhi	49153122	\N	\N	kk kohli	delhi	4	99acres	https://www.99acres.com/4-bhk-bedroom-independent-builder-floor-for-sale-in-janakpuri-west-delhi-3200-sq-ft-spid-N86574416	2026-04-21	\N	t	6653268c235e5825191a2fd9617c00d6	2026-04-20 16:26:37.546025	2026-04-21 12:20:31.191378
54	88184e0d3474e95bcfcfa71337c8cff5	3 BHK Builder Floor in Kailash hills, Delhi	32253971	\N	\N	Kailash hills, Delhi, South Delhi	delhi	3	99acres	https://www.99acres.com/3-bhk-bedroom-independent-builder-floor-for-sale-in-kailash-hills-south-delhi-1260-sq-ft-spid-X89620016	2026-04-21	\N	t	f646d58870fdc21e11572e0dd611fd19	2026-04-21 12:09:44.931587	2026-04-21 12:20:31.191378
55	455e60a625749b19b40a3169399fcab5	\N	98500000	\N	3200	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	5ead8c713a27fbdef8c443dc952ced34	2026-04-20 16:25:58.788003	2026-04-21 12:20:31.191378
56	ade9e1a2427ac5bb3037a814302b1553	\N	110100000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	d804c11f93326ed6f67c768dc31de343	2026-04-20 16:25:59.467165	2026-04-21 12:20:31.191378
57	632549487fc23ffdb2ff8e266aa39c9b	\N	62500000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	341f730bdaf482a20f27a3a9fcb4437a	2026-04-20 16:26:00.058349	2026-04-21 12:20:31.191378
58	c02f5cd0f7e0b5f36e316b9b1683ce61	\N	17900000	\N	1200	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	ff3b68bca5b0b58c774e320320f6d088	2026-04-20 16:26:00.434829	2026-04-21 12:20:31.191378
60	d1a006e794b333121533cd8bb3fbf594	\N	28500000	\N	200	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	d8f009a548e4d4e827dd809f674f140a	2026-04-20 16:26:01.038154	2026-04-21 12:20:31.191378
61	e9ecb85166da858f13ce01a5d620b9fc	\N	173500000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	f061d829238caae4518459c1466c0c6e	2026-04-20 16:26:01.385023	2026-04-21 12:20:31.191378
62	d1c49fe2ebc6773a266ab106bdbc3214	\N	135000000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	96deccd76f45a7c8b24e7dd6306c0921	2026-04-20 16:26:01.638955	2026-04-21 12:20:31.191378
63	98551963ddbe15707e0f15b758c830a7	\N	29900000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	661a2c44ecd0da6851b8a5e9d28b20c9	2026-04-20 16:26:01.887381	2026-04-21 12:20:31.191378
64	ec91da088c6aa20a040ea24f5a272f0f	\N	75000000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	9970b8e354b18144e8f233cedac5bd87	2026-04-20 16:26:02.267148	2026-04-21 12:20:31.191378
65	f7f68ffbe1d4ff921a95fad122c91a3d	\N	39000000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	3501c0202f0f27a045c55168483b36be	2026-04-20 16:26:02.568437	2026-04-21 12:20:31.191378
66	71b462731b305c07c572b6b6283caca5	\N	80000000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	ad2046f99a36ec5bb2d0dc7211b9b80f	2026-04-20 16:26:02.837074	2026-04-21 12:20:31.191378
59	021abfcb2a6bef353d87160b9e0027ec	\N	24800000	\N	1700	\N	delhi	\N	magicbricks	\N	2026-04-21	2026-04-21	f	e3c0f6dc789c4aceda72d4f9a96ae7c6	2026-04-20 16:26:00.738339	2026-04-21 12:20:31.191378
67	021abfcb2a6bef353d87160b9e0027ec	\N	24800000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	af10f899ea4cdce72232b7ba99316d26	2026-04-20 16:26:03.055535	2026-04-21 12:20:31.191378
68	0143e4f2d75fef68760a90b7d2643fcb	\N	120000000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	7883f77f25e021c976d877acf11bf61d	2026-04-20 16:26:03.354782	2026-04-21 12:20:31.191378
69	73d89cb9e993a3865ceb2f9459c243ff	\N	6000000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	1e983993750153db5f9fbfb05dddc197	2026-04-20 16:26:03.622469	2026-04-21 12:20:31.191378
70	6b58337b5fbedfc46800b78a9944f535	\N	5000000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	9863da4518db7aeb257b4e67e0bd455a	2026-04-20 16:26:03.904814	2026-04-21 12:20:31.191378
71	8ced9fcf803088b361eaece9d4c51c0b	\N	4500000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	f875a99ed5ee1ce8fd05f8db8dc8db7b	2026-04-20 16:26:04.203991	2026-04-21 12:20:31.191378
72	f7590241d021dfedd20d942f304d4287	\N	34500000	\N	2200	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	2383797baca5533560b04f58d422257d	2026-04-20 16:26:04.604107	2026-04-21 12:20:31.191378
73	4c4360afaf089ce1e2b268c63672e7b5	\N	29500000	\N	1700	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	9c1652fca78db19d2ac16bd3761ecab1	2026-04-21 12:09:26.317621	2026-04-21 12:20:31.191378
74	fa886d86532b9c2c210180d5cf6a0fdc	\N	17500000	\N	100	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	2cba3bad37d7dbb39b0ca4eb129f3287	2026-04-21 12:09:26.755646	2026-04-21 12:20:31.191378
75	e8ee04c3574e767337135b3fd98895e9	\N	37500000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	16d4901457d76a83263b7c81b0da3c63	2026-04-21 12:09:28.134407	2026-04-21 12:20:31.191378
76	75e1dbabd8a31a850bc90c1db35ff06e	\N	32500000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	dc944f6e3dacccc8a04cd2f6ae53c1a3	2026-04-21 12:09:28.806189	2026-04-21 12:20:31.191378
77	cbbbc31ae2558fb0a379dc1f20ec6085	\N	5500000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	9f1a5b7d71d7c96a151e642357960aa8	2026-04-21 12:09:29.003528	2026-04-21 12:20:31.191378
78	1a07934ff854ff03cf5ac18644f33ea2	\N	2700000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	af2778d16393d60d63b57cd70808a68a	2026-04-21 12:09:29.187397	2026-04-21 12:20:31.191378
79	04c3c5ab407389960fa250fd9fba2c47	\N	26000000	\N	NaN	\N	delhi	\N	magicbricks	\N	2026-04-21	\N	t	d48782f7d353ecaf38c0b049a5ff0482	2026-04-21 12:09:29.401957	2026-04-21 12:20:31.191378
80	861bdde7603da1b68012c54ef174a72b	3 BHK Builder Floor for Sale in Vikas Puri, Delhi	18000000	\N	\N	Vikas Puri, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	a3d0a0cd7853092f1fb93ab55d3dbc13	2026-04-20 16:27:08.188065	2026-04-21 12:20:31.191378
114	0dafe84e6628ee755879c16cb32ccba0	\N	57800000	\N	2700	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	3290df6e2b103676561eb4da73cc7e94	2026-04-20 16:25:00.412262	2026-04-21 12:20:31.191378
115	84309af7b74581fdc07667e36aa289f3	\N	81300000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	f4ee3ca2d0cc4c1e3d405b948b62d863	2026-04-20 16:25:00.54549	2026-04-21 12:20:31.191378
81	029489b95a4360bbb6f27f3990d7db39	3, 4 BHK Flats in\nEldeco Camelot\nSector 17 Dwarka, Delhi\nStarting From\n₹ 7.42 Cr\n+ Charges	74200000	\N	\N	Starting From\n₹ 7.42 Cr\n+ Charges	delhi	4	squareyards	https://www.squareyards.com/delhi-residential-property/eldeco-camelot/343088/project	2026-04-21	\N	t	0f360b413297f3556efe359abefd66a4	2026-04-20 16:27:08.294645	2026-04-21 12:20:31.191378
82	2c3a2e57d35abde21aa055fd3e0fc157	2 BHK House for Sale in Dwarka Mor, Delhi	9500000	\N	\N	Dwarka Mor, Delhi	delhi	2	squareyards	NaN	2026-04-21	\N	t	8edbfb9fda138d17a7ddad1efc48e322	2026-04-20 16:27:08.370673	2026-04-21 12:20:31.191378
83	6b6bacae36ee92e64ee2abea1d699bd3	4 BHK Builder Floor for Sale in Panchsheel Vihar, Delhi	15000000	\N	\N	Panchsheel Vihar, Delhi	delhi	4	squareyards	NaN	2026-04-21	\N	t	9c35da3642ef6a0aab605b3908b90812	2026-04-20 16:27:08.438731	2026-04-21 12:20:31.191378
84	1586bea60ec68c7a7a1fd88d09129a21	3 BHK Builder Floor for Sale in Shivalik Colony, Delhi	55000000	\N	\N	Shivalik Colony, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	cbf06b4c35b94ca680c39017ea8fca19	2026-04-20 16:27:08.522936	2026-04-21 12:20:31.191378
85	eddff2d892ad377e97d6e8ebd7f62dbb	3 BHK Builder Floor for Sale in Greater Kailash I, Delhi	66500000	\N	\N	Greater Kailash I, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	3ff72243c45ffe122314bfa8dc4eb12d	2026-04-20 16:27:08.609893	2026-04-21 12:20:31.191378
86	91f3f545798d8862caffc2f24b211a6e	3 BHK Builder Floor for Sale in Maidan Garhi, Delhi	7500000	\N	\N	Maidan Garhi, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	3e01a1bd5b033d96220f1d9011c85d7f	2026-04-20 16:27:08.676355	2026-04-21 12:20:31.191378
87	54e494c65c8e0589547570f5b4927299	3 BHK Builder Floor for Sale in Vasant Vihar, Delhi	90000000	\N	\N	Vasant Vihar, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	4212421aca975078d1638d83f03f4d6c	2026-04-20 16:27:08.735597	2026-04-21 12:20:31.191378
88	b82fbfe329858e9940dc7d5dc7465152	5 BHK Builder Floor for Sale in Basant Lok, Delhi	340000000	\N	\N	Basant Lok, Delhi	delhi	5	squareyards	NaN	2026-04-21	\N	t	ca5a8ba7f3e0c8f2d5b56f5cf73fce3d	2026-04-20 16:27:08.870484	2026-04-21 12:20:31.191378
89	9e477e29f68c0d1e7ed071745b85aa59	3 BHK Builder Floor for Sale in Lajpat Nagar Iii, Delhi	70000000	\N	\N	Lajpat Nagar Iii, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	74616c180ff0265706372c57cc1d220b	2026-04-20 16:27:08.941811	2026-04-21 12:20:31.191378
90	621b0d5ef31007d1a2ff93228b2755e4	4 BHK Flat for Sale in Anand Vihar, Delhi	35000000	\N	\N	Anand Vihar, Delhi	delhi	4	squareyards	NaN	2026-04-21	\N	t	e91328d4522ebc8cf8e63504932ff806	2026-04-20 16:27:09.010316	2026-04-21 12:20:31.191378
91	fd0eb37fb5c5a69c8c8ccdfebeac8982	3 BHK Builder Floor for Sale in Rajouri Garden, Delhi	28000000	\N	\N	Rajouri Garden, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	7d1520ffb126eb24643cf25634826866	2026-04-20 16:27:09.066148	2026-04-21 12:20:31.191378
92	041eca2292dbf8ab47bd67b25e896735	Land for Sale in Chattarpur, Delhi	125000000	\N	\N	1251 Sq.Yd.	delhi	\N	squareyards	NaN	2026-04-21	\N	t	2c4d96f800cc8ab8810aaa33109770ee	2026-04-20 16:27:09.531019	2026-04-21 12:20:31.191378
93	96632bd4a07b17e78f9ba5f51a1a96e9	3 BHK Builder Floor for Sale in Malviya Nagar, Delhi	35000000	\N	\N	Malviya Nagar, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	e91328d4522ebc8cf8e63504932ff806	2026-04-20 16:27:09.610851	2026-04-21 12:20:31.191378
94	0a921f233bc38381c8611ad7d38bb135	2 BHK Builder Floor for Sale in Rohini Sector 25, Delhi	7000000	\N	\N	Rohini Sector 25, Delhi	delhi	2	squareyards	NaN	2026-04-21	\N	t	d70b0f1a512ba76532b531c42a3fd452	2026-04-21 12:10:12.097082	2026-04-21 12:20:31.191378
95	8ca5c3b4a541ac3f09360b1229bed34e	3 BHK Flat for Sale in Sector 5 Dwarka, Delhi	35000000	\N	\N	Sector 5 Dwarka, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	e91328d4522ebc8cf8e63504932ff806	2026-04-21 12:10:12.250708	2026-04-21 12:20:31.191378
96	9b544250f89db2cac58e36c426ae9742	2 BHK Builder Floor for Sale in Lajpat Nagar I, Delhi	26500000	\N	\N	Lajpat Nagar I, Delhi	delhi	2	squareyards	NaN	2026-04-21	\N	t	2072f65cd4690b18d0be912dfb7a8683	2026-04-21 12:10:12.344197	2026-04-21 12:20:31.191378
97	91163b31b82c8791b0c1958996413217	4 BHK Flat for Sale in Greater Kailash, Delhi	85000000	\N	\N	Greater Kailash, Delhi	delhi	4	squareyards	NaN	2026-04-21	\N	t	cca4654ce7e7ebc1a25152cfd17574b4	2026-04-21 12:10:12.439769	2026-04-21 12:20:31.191378
98	a5d4d66636c1d5c79e5f411b1c4c4ee6	4 BHK Flat for Sale in Greater Kailash I, Delhi	170000000	\N	\N	Greater Kailash I, Delhi	delhi	4	squareyards	NaN	2026-04-21	\N	t	8e1d9f318992380f27d6447e475c8dd0	2026-04-21 12:10:12.538668	2026-04-21 12:20:31.191378
99	539609e482d98452bfe76b39c425d85d	3 BHK Flat for Sale in Sector 12 Dwarka, Delhi	25000000	\N	\N	Sector 12 Dwarka, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	36a52d823345f5b3b8e6ce8b2ae0a06a	2026-04-21 12:10:12.668838	2026-04-21 12:20:31.191378
100	503d8913f0454d9bb32f4293e7ba6811	3 BHK Builder Floor for Sale in Chattarpur, Delhi	8600000	\N	\N	Chattarpur, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	e24ae67dee5ea642f883fad204717fe2	2026-04-21 12:10:12.787238	2026-04-21 12:20:31.191378
101	8791be67ac6cc75d0a13558d85d892d6	3 BHK Builder Floor for Sale in Dera Mandi, Delhi	7500000	\N	\N	Dera Mandi, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	3e01a1bd5b033d96220f1d9011c85d7f	2026-04-21 12:10:12.913453	2026-04-21 12:20:31.191378
102	d761f86de683149d1d8b45fdfe5ed5b5	3 BHK Flat for Sale in Dwarka, Delhi	29100000	\N	\N	Dwarka, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	efdec36ee1d62ce5d0bf04de6bb95216	2026-04-21 12:10:12.996326	2026-04-21 12:20:31.191378
103	65b2c3bc00fd5878add85c8a17b54e4e	4 BHK Builder Floor for Sale in Greater Kailash I, Delhi	70000000	\N	\N	Greater Kailash I, Delhi	delhi	4	squareyards	NaN	2026-04-21	\N	t	74616c180ff0265706372c57cc1d220b	2026-04-21 12:10:13.607962	2026-04-21 12:20:31.191378
104	175a05176f6e6eaaf1189a6863b37660	3 BHK Flat for Sale in Safdarjung Enclave, Delhi	57500000	\N	\N	Safdarjung Enclave, Delhi	delhi	3	squareyards	NaN	2026-04-21	\N	t	ace5e4180f5b15799e09a5e3bce55205	2026-04-21 12:10:13.719188	2026-04-21 12:20:31.191378
105	ce83f5497dd110db2af49b1cddcdcfe7	3.5 BHK Builder Floor for Sale in Malviya Nagar, Delhi	42500000	\N	\N	Malviya Nagar, Delhi	delhi	5	squareyards	NaN	2026-04-21	\N	t	5cf04af8bc2ad363d1bb28d26b1cb37d	2026-04-21 12:10:13.828993	2026-04-21 12:20:31.191378
106	db90724495e8f8b08801b87801112a57	3 BHK Flat in Sector 63A, Gurgaon	63396721	\N	\N	TARC Ishva	gurugram	3	99acres	https://www.99acres.com/3-bhk-bedroom-apartment-flat-for-sale-in-tarc-ishva-sector-63a-gurgaon-1588-sq-ft-spid-A89505390	2026-04-21	\N	t	791e0ecf81b554fc3986f64c50b1294c	2026-04-20 16:25:22.639626	2026-04-21 12:20:31.191378
107	474ce557bdfc8ed982555a9a98d25dbd	3 BHK Flat in Sector 85, Gurgaon	30815000	\N	\N	Ganga Anantam	gurugram	3	99acres	https://www.99acres.com/3-bhk-bedroom-apartment-flat-for-sale-in-sector-85-gurgaon-2051-sq-ft-spid-G89007232	2026-04-21	\N	t	00ddf8b770ae4a0099ca928a89b9a5a2	2026-04-20 16:25:24.604087	2026-04-21 12:20:31.191378
108	2a57bf9c357801dfd4557dccbf34eb8f	4 BHK Independent Builder Floor in Sushant Lok Phase 1, Gurgaon	52516406	\N	\N	Luxury Builder Floor In Sushant Lok 1	gurugram	4	99acres	https://www.99acres.com/4-bhk-bedroom-independent-builder-floor-for-sale-in-luxury-builder-floor-in-sushant-lok-1-sushant-lok-phase-1-gurgaon-3200-sq-ft-spid-C90532404	2026-04-21	\N	t	a1fd7c4765e9fcb8514a9816a322b542	2026-04-21 12:08:54.863891	2026-04-21 12:20:31.191378
109	c1eff59b93b2687fb0858dda10720c65	\N	734100000	\N	7196	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	03023e4faa95da1daa8b1e1e4389667b	2026-04-20 16:24:59.367758	2026-04-21 12:20:31.191378
110	168821f6ca38dbc295050d1c346971c9	\N	19700000	\N	1550	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	cecb1284677929e754d395dacf699ff3	2026-04-20 16:24:59.563944	2026-04-21 12:20:31.191378
111	18fb3c8bff0f82b62629615eb3b2a381	\N	36500000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	26beb1bfdbcaa4ec5b34c4ac33439982	2026-04-20 16:24:59.699191	2026-04-21 12:20:31.191378
112	88d2a0ac350445bf4c4902f837ff210d	\N	26600000	\N	1420	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	b8cf9c87968143a2016e59795f8e9e4d	2026-04-20 16:25:00.151465	2026-04-21 12:20:31.191378
113	3fbe3bb7865df1e9bf7de927a17d5e72	\N	35000000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	81eabbd07a0bcaa21217017a52b98c2c	2026-04-20 16:25:00.259294	2026-04-21 12:20:31.191378
116	0c080510d2642f0ac5aa72d2f9958637	\N	98900000	\N	2874	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	d9d75a3dd7d847024ae609acfa1381ad	2026-04-20 16:25:00.830395	2026-04-21 12:20:31.191378
117	f3d7ce9471cae2513c58b5060ea7f42e	\N	34000000	\N	2450	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	9e3f1011a8933dde79c8675eb9e41b45	2026-04-20 16:25:00.944227	2026-04-21 12:20:31.191378
118	c6f8251702f6559612bf29a6e3d31f4a	\N	70500000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	57a99553f8e14462e5462df8c74badcc	2026-04-20 16:25:01.066111	2026-04-21 12:20:31.191378
119	bb0d68ee6bee76854f332cd1cf2b8622	\N	25600000	\N	1999	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	33c351047ba06fefef16521d2237804a	2026-04-20 16:25:01.398034	2026-04-21 12:20:31.191378
120	4ed77ad8a796de8254bfbf17f879e10e	\N	12500000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	9233e63590609d5f6419f137b087a775	2026-04-20 16:25:01.527813	2026-04-21 12:20:31.191378
121	a34a8a8dc674c6d58738efe1d6157f53	\N	37300000	\N	2298	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	690fe9053b1889671c3d2aecbb91c358	2026-04-20 16:25:01.696282	2026-04-21 12:20:31.191378
122	99d013c948f87f21bc03ec0ece34daa1	\N	27800000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	55fecc85f5c3495f10c743c4107f5911	2026-04-20 16:25:01.844146	2026-04-21 12:20:31.191378
123	91d68db997b435e35ecacced420c2827	\N	41200000	\N	2333	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	a5ac8e03b426136a4faf961aa616688b	2026-04-20 16:25:01.994123	2026-04-21 12:20:31.191378
124	316c3c6f0183a14831aa60f7922505cf	\N	22500000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	9c5be06cef550d10671919af311ae8b7	2026-04-20 16:25:02.313211	2026-04-21 12:20:31.191378
125	ea4900089bc178c5bd58680cf82999c6	\N	25500000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	c678e45c5534888a6b3a902572d70780	2026-04-20 16:25:02.463412	2026-04-21 12:20:31.191378
126	ffb422d76e3fa8a69078b0ea2987b10a	\N	969200000	\N	9500	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	e78b559ca8b3e2884e12d40ea3eae194	2026-04-21 12:08:29.764041	2026-04-21 12:20:31.191378
127	1d37ddcd50f230c32c5605ffa2a53586	\N	28500000	\N	1902	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	5d8f6e943452e4104a3dd015f0c55708	2026-04-21 12:08:30.210723	2026-04-21 12:20:31.191378
128	aae220ded1239d8f502181e0203673c7	\N	369400000	\N	5850	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	917d2b3556616b227f736458d096d1e9	2026-04-21 12:08:30.453849	2026-04-21 12:20:31.191378
129	77e2cf8e282e13091c6bb7992175791e	\N	100100000	\N	3956	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	e228c72a8219c928229fca2749f9bc0d	2026-04-21 12:08:30.626604	2026-04-21 12:20:31.191378
130	89bd53d5147e71ac6ab899574e614371	\N	24000000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	9c1256c3fc89f0283f8b0de49391d588	2026-04-21 12:08:30.801324	2026-04-21 12:20:31.191378
131	854ecca8d4412c8bb46a64733acfe295	\N	38600000	\N	2495	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	169cf81cdfc8fb9739428973f04c4ec2	2026-04-21 12:08:30.894235	2026-04-21 12:20:31.191378
132	149ff3f670d2f38cc1c402450ae88cec	\N	19000000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	954b2c31bd19d64a3b12ee34117b1d49	2026-04-21 12:08:30.967444	2026-04-21 12:20:31.191378
133	272cb6b0d94a6689ae7281d628e4fa68	\N	47000000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	a83aed3acc5d61054d4357ffc82d5316	2026-04-21 12:08:31.194406	2026-04-21 12:20:31.191378
134	88438cfc4824c003171d696deb059b2d	\N	33400000	\N	2060	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	ce1ea90864107faf375c0280d1c1feb4	2026-04-21 12:08:31.285051	2026-04-21 12:20:31.191378
135	b6d795e17bad64d142ad8b1746a018a5	\N	51400000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	0854cf53d0dfb8fb67c53828affcbea5	2026-04-21 12:08:31.415665	2026-04-21 12:20:31.191378
136	f31f15ac9a33dad5385dec5c83d950de	\N	36200000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	e1da44fef941aca9e7f8442608d8aaf0	2026-04-21 12:08:31.61224	2026-04-21 12:20:31.191378
137	862e52ea94b008e2a54a2226f1aa0dd5	\N	44500000	\N	NaN	\N	gurugram	\N	magicbricks	\N	2026-04-21	\N	t	cd26b61035b7ac5a4f9e0445cb97819a	2026-04-21 12:08:31.694	2026-04-21 12:20:31.191378
138	baa5e1e617545be41eaa1ff33ed58a4f	3 BHK Flat for Sale in Sector 72, Gurgaon	24000000	\N	\N	1975 Sq.Ft.	gurugram	3	squareyards	NaN	2026-04-21	\N	t	d3d6b2aab7054c68e93f0fae6b53aab5	2026-04-20 16:25:43.970668	2026-04-21 12:20:31.191378
139	9d4b41fe55a52cbb773fdcd740951c99	3 BHK Flat for Sale in Sector 79, Gurgaon	22500000	\N	\N	1490 Sq.Ft.	gurugram	3	squareyards	NaN	2026-04-21	\N	t	7679d400a6f09135cf9a363b8aa4ae9f	2026-04-20 16:25:44.266752	2026-04-21 12:20:31.191378
140	882d57ab8a3a55f937fd1ec0ce6811cf	2.5 BHK Builder Floor for Sale in Sector 95a, Gurgaon	10800000	\N	\N	1437 Sq.Ft.	gurugram	5	squareyards	NaN	2026-04-21	\N	t	7b88fe4722b54b6d52393459975888e7	2026-04-20 16:25:44.434071	2026-04-21 12:20:31.191378
141	0d109115b8a534d749581acc1eb1976f	5 BHK Builder Floor for Sale in Dlf Phase ii, Gurgaon	48500000	\N	\N	316 Sq.Yd.	gurugram	5	squareyards	NaN	2026-04-21	\N	t	9aa69065d0609d7161eed0696808feb7	2026-04-20 16:25:44.584919	2026-04-21 12:20:31.191378
142	48bef6578301bb94e27f0b9df64bc055	4 BHK Flat for Sale in Sector 112, Gurgaon	87000000	\N	\N	4350 Sq.Ft.	gurugram	4	squareyards	NaN	2026-04-21	\N	t	934ea04aa74d77d83d1ce23ad5cf84da	2026-04-20 16:25:44.814902	2026-04-21 12:20:31.191378
143	5932d8b76454ce746b72a1c451e445c4	4 BHK Builder Floor for Sale in Sector 67a, Gurgaon	31000000	\N	\N	270 Sq.Ft.	gurugram	4	squareyards	NaN	2026-04-21	\N	t	e905750ff93b18e1cdf1d60a6f3f7b34	2026-04-20 16:25:44.917728	2026-04-21 12:20:31.191378
144	7d69d6ed7a527f76c8b6fa30a194ddf2	2 BHK Flat for Sale in Dlf Phase iv, Gurgaon	22500000	\N	\N	1105 Sq.Ft.	gurugram	2	squareyards	NaN	2026-04-21	\N	t	7679d400a6f09135cf9a363b8aa4ae9f	2026-04-20 16:25:45.041121	2026-04-21 12:20:31.191378
145	2673a89e40420323d3809281cdc5e46f	4 BHK Villa for Sale in Sector 48, Gurgaon	165000000	\N	\N	500 Sq.Yd.	gurugram	4	squareyards	NaN	2026-04-21	\N	t	ff39129499583a00092e36f36486fe35	2026-04-20 16:25:45.299592	2026-04-21 12:20:31.191378
146	447268c15655573a08f4d44fe73ffa25	1 RK Flat for Sale in Sohna Sector 35, Gurgaon	9000000	\N	\N	1021 Sq.Ft.	gurugram	\N	squareyards	NaN	2026-04-21	\N	t	1e0b5a52fa4a91b42754c547c6d68b1b	2026-04-20 16:25:45.434781	2026-04-21 12:20:31.191378
147	0ec4f243515569c06d5b850c3995b1fc	3 BHK Flat for Sale in Sector 61, Gurgaon	25800000	\N	\N	1680 Sq.Ft.	gurugram	3	squareyards	NaN	2026-04-21	\N	t	bcb79b4bd3b784c6fdbcd14667f1ef2f	2026-04-20 16:25:45.585488	2026-04-21 12:20:31.191378
148	c2944dd261a7614379b510d75a855111	DLF Central 84\nSector 84, Gurgaon	99000000	\N	\N	Sector 84, Gurgaon	gurugram	\N	squareyards	https://www.squareyards.com/gurgaon-residential-property/dlf-central-84/339877/project	2026-04-21	\N	t	f3f99ad3321cf5b916e98bc71e1a3190	2026-04-20 16:25:45.836986	2026-04-21 12:20:31.191378
149	98e7ce0ffbaccfd205cc41f6966811f8	Adani Veris\nGwal Pahari, Gurgaon	206500000	\N	\N	Gwal Pahari, Gurgaon	gurugram	\N	squareyards	https://www.squareyards.com/gurgaon-residential-property/adani-veris/339461/project	2026-04-21	\N	t	e573c11f22f0dc8b96a50378d2f24ada	2026-04-20 16:25:46.420916	2026-04-21 12:20:31.191378
150	1cc95885d3149650dae41baf703d2525	Tulip Melrose\nSector 70, Gurgaon	48200000	\N	\N	Sector 70, Gurgaon	gurugram	\N	squareyards	https://www.squareyards.com/gurgaon-residential-property/tulip-melrose/342051/project	2026-04-21	\N	t	d9c9aa2a1dea515d8e723c032b1a3db4	2026-04-20 16:25:47.703386	2026-04-21 12:20:31.191378
151	d962e9cc5754ade65b54abd6f8a98963	2.5 BHK Flat for Sale in Sector 70a, Gurgaon	23200000	\N	\N	1642 Sq.Ft.	gurugram	5	squareyards	NaN	2026-04-21	\N	t	b6ece0dcb0d758daecebdc80c8c6cbf1	2026-04-21 12:09:12.998867	2026-04-21 12:20:31.191378
152	59e69852fe6ae676c370690e954676ee	3 BHK Flat for Sale in Sector 102, Gurgaon	37500000	\N	\N	1689 Sq.Ft.	gurugram	3	squareyards	NaN	2026-04-21	\N	t	9bdff2bb5e02511d7ba94bbbb18406c1	2026-04-21 12:09:13.284969	2026-04-21 12:20:31.191378
153	fc54480c0f57e05c0b9974ab0a36a82d	4 BHK Flat for Sale in Sector 42, Gurgaon	279000000	\N	\N	7196 Sq.Ft.	gurugram	4	squareyards	NaN	2026-04-21	\N	t	fa961cec754879a75c0113a86302c61e	2026-04-21 12:09:13.440486	2026-04-21 12:20:31.191378
154	8005747b610458d096f9e83e5bbccf75	4 BHK Flat for Sale in Sector 90, Gurgaon	24100000	\N	\N	2356 Sq.Ft.	gurugram	4	squareyards	NaN	2026-04-21	\N	t	44268e2edecddeb8cee14d186326a59e	2026-04-21 12:09:13.60122	2026-04-21 12:20:31.191378
155	1a47eae9ef8a61da22f75bbd170c5a90	3 BHK Flat for Sale in Sector 68, Gurgaon	30000000	\N	\N	1950 Sq.Ft.	gurugram	3	squareyards	NaN	2026-04-21	\N	t	4942d2f03078083532f785b3421c2b45	2026-04-21 12:09:13.89197	2026-04-21 12:20:31.191378
156	63bc8b811ec74d44a347f7abee384130	3 BHK Builder Floor for Sale in Sector 51, Gurgaon	33000000	\N	\N	2160 Sq.Ft.	gurugram	3	squareyards	NaN	2026-04-21	\N	t	8a0d8b207ca194a1fa9c5c784238df63	2026-04-21 12:09:14.034006	2026-04-21 12:20:31.191378
\.


--
-- Name: listings_history_id_seq; Type: SEQUENCE SET; Schema: silver; Owner: postgres
--

SELECT pg_catalog.setval('silver.listings_history_id_seq', 156, true);


--
-- PostgreSQL database dump complete
--

\unrestrict 92Bl1TChd3uwqaffCFMazS2Q58qETTQGFUCp3INCbNyEjcZS6QgyDXM3krN3FhZ

