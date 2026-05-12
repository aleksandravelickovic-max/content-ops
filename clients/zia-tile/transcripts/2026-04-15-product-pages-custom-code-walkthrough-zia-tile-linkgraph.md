---
title: Product Pages Custom Code Walkthrough – Zia Tile/LinkGraph
date: 2026-04-15
source: csm-curated-transcript
client: Zia Tile
attendees: ["Alex Belanger", "Devyn Grenner", "Jamie Greenspan", "Marissa Hill-Whitson"]
recording_url: https://app.clickup.com/9011399348/docs/8chy2nm-1697791
original_section: "5. Product Pages Custom Code Walkthrough – Zia Tile/LinkGraph"
---

# **5\. Product Pages Custom Code Walkthrough – Zia Tile/LinkGraph**

**Date:** April 15, 2026

**Attendees:** Alex Belanger, Devyn Grenner, Jamie Greenspan, Marissa Hill-Whitson

## **Overview**

Technical walkthrough of Liquid files, Accentuate, and meta objects for product pages, emphasizing SEO optimization and risk management for live updates.

 

## **Transcript:**

* **Alex Belanger:** Hey Marissa, how are you  
  * **Marissa Hill-Whitson:** Good. How are you feeling?  
  * **Alex Belanger:** Powering through? Powering through. Yeah, no, I took a bunch of like meds for this call to make sure I'd be okay for it. So it should be good.  
  * **Marissa Hill-Whitson:** Yeah, fair.  
  * **Alex Belanger:** Yeah, it's honestly it's mostly, it's mostly just exhaustion. Like I had horrible sleep last night. I got maybe like two hours and I've been up since like 4am  
  * **Marissa Hill-Whitson:** Ew.  
  * **Alex Belanger:** I know. So it's just been one of those. So that's why I've still been kind of able to respond online  
  * **Marissa Hill-Whitson:** Yeah,  
  * **Alex Belanger:** there. It's just been like. And of course I had this call coming up so I was like I can't  
  * **Marissa Hill-Whitson:** I  
  * **Alex Belanger:** even nap.  
  * **Marissa Hill-Whitson:** know. I saw  
  * **Alex Belanger:** Like.  
  * **Marissa Hill-Whitson:** your offline and I was like,  
  * **Alex Belanger:** Yeah, no, I forgot to let you know that  
  * **Marissa Hill-Whitson:** just  
  * **Alex Belanger:** for  
  * **Marissa Hill-Whitson:** like,  
  * **Alex Belanger:** sure.  
  * **Marissa Hill-Whitson:** instant  
  * **Alex Belanger:** No, I  
  * **Marissa Hill-Whitson:** panic.  
  * **Alex Belanger:** wasn't. No,  
  * **Marissa Hill-Whitson:** Like, are  
  * **Alex Belanger:** no,  
  * **Marissa Hill-Whitson:** you abandoning me?  
  * **Alex Belanger:** no. I could be in the hospital. I'm taking a zeal. No worries.  
  * **Marissa Hill-Whitson:** Yeah, I got it. Love it. Just a little line. Did you read my screenshot about how I think the site is currently set up with, like, the product information? She's not here yet, is she?  
  * **Alex Belanger:** No, no, no, you're good, you're good.  
  * **Marissa Hill-Whitson:** Okay. Basically, like, I looked into the main product, like, Liquid File, because I used to. I used to build shop sites. This is the only platform  
  * **Alex Belanger:** Oh  
  * **Marissa Hill-Whitson:** I'm  
  * **Alex Belanger:** okay.  
  * **Marissa Hill-Whitson:** familiar with.  
  * **Alex Belanger:** Nice,  
  * **Marissa Hill-Whitson:** So I was  
  * **Alex Belanger:** nice.  
  * **Marissa Hill-Whitson:** looking at it and I was like, it appears that they have, like, a fundamental setup for, like, every single product that's on every single page. So I just wanted to flag that. I think that this is how it's set up, and if it is the case, we need to get alignment that. That's fine. To roll it on all products or  
  * **Alex Belanger:** Oh  
  * **Marissa Hill-Whitson:** do we  
  * **Alex Belanger:** yeah.  
  * **Marissa Hill-Whitson:** keep,  
  * **Alex Belanger:** Oh that  
  * **Marissa Hill-Whitson:** like.  
  * **Alex Belanger:** part already tackled or I emailed them about it.  
  * **Marissa Hill-Whitson:** Okay,  
  * **Alex Belanger:** So I gave them that three bullet points that you sent beforehand.  
  * **Marissa Hill-Whitson:** yeah,  
  * **Alex Belanger:** I didn't give the full detail the liquid stuff, but  
  * **Marissa Hill-Whitson:** yeah,  
  * **Alex Belanger:** just saying that it seems to be a site wide thing for  
  * **Marissa Hill-Whitson:** yeah.  
  * **Alex Belanger:** every  
  * **Marissa Hill-Whitson:** Like,  
  * **Alex Belanger:** product  
  * **Marissa Hill-Whitson:** from  
  * **Alex Belanger:** page.  
  * **Marissa Hill-Whitson:** what I can gather if I'm wrong, like, that's fine. But  
  * **Alex Belanger:** Yeah. Which I think it should be fine. They want to be doing it for every product page  
  * **Marissa Hill-Whitson:** yeah,  
  * **Alex Belanger:** from my understanding. But  
  * **Marissa Hill-Whitson:** yeah,  
  * **Alex Belanger:** we'll get a line on the call here.  
  * **Marissa Hill-Whitson:** okay.  
  * **Alex Belanger:** Devin  
  * **Marissa Hill-Whitson:** Cool,  
  * **Alex Belanger:** just joined in. So Devin is their internal web person basically.  
  * **Marissa Hill-Whitson:** cool. We can bond over that. Even though I don't develop things.  
  * **Alex Belanger:** That's all good. Hey there Devin. How are you?  
  * **Marissa Hill-Whitson:** Hi,  
  * **Devyn Grenner:** Good. How are you? Hi.  
  * **Alex Belanger:** Doing quite well, thanks. Doing quite well. I don't, I don't believe we've properly met yet. Eh. I  
  * **Devyn Grenner:** Yeah,  
  * **Alex Belanger:** think. Were you on the.  
  * **Devyn Grenner:** I  
  * **Alex Belanger:** Were  
  * **Devyn Grenner:** was.  
  * **Alex Belanger:** you  
  * **Devyn Grenner:** But  
  * **Alex Belanger:** on the kickoff?  
  * **Devyn Grenner:** I was.  
  * **Alex Belanger:** Oh, okay. Gotcha,  
  * **Devyn Grenner:** I was like silently in the background.  
  * **Alex Belanger:** gotcha. Okay. Sorry  
  * **Devyn Grenner:** Yeah,  
  * **Alex Belanger:** about that.  
  * **Devyn Grenner:** yeah, no, it's okay. Nice to meet you.  
  * **Marissa Hill-Whitson:** nice to meet you. I know we haven't met. No, it's  
  * **Devyn Grenner:** Yeah.  
  * **Marissa Hill-Whitson:** lovely to meet  
  * **Devyn Grenner:** Yeah,  
  * **Marissa Hill-Whitson:** you.  
  * **Devyn Grenner:** I. I manage the website  
  * **Marissa Hill-Whitson:** Okay.  
  * **Devyn Grenner:** and  
  * **Marissa Hill-Whitson:** Yeah. I'm  
  * **Devyn Grenner:** work  
  * **Marissa Hill-Whitson:** the  
  * **Devyn Grenner:** that.  
  * **Marissa Hill-Whitson:** director of Web operations and Delivery here, so  
  * **Devyn Grenner:** Great.  
  * **Marissa Hill-Whitson:** I. I handle our technical team that does edits when required.  
  * **Devyn Grenner:** Cool. Meet you.  
  * **Alex Belanger:** Yeah, I believe we're just waiting on Jamie but we could probably get started because we're basically just Devin. Hopefully you can give us a rundown on the code backend. Just want to make sure that we have firm idea of how it works. Anytime it's custom code, we want to make sure that anything we do won't break anything. Just best practices there. But yeah. Do you want to maybe share your screen? Can maybe kind of walk me Marissa through it and we can get like a better sense.  
  * **Devyn Grenner:** Yeah, I. I was on. I saw the last few parts of the thread, the email thread, and I know that we're looking into updating product detail copy, but I. I want to make sure I'm showing you exactly what you need. Are we. We just want to see essentially how we're adding detail or copy essentially on the product pages. Is that right? Is there anything  
  * **Marissa Hill-Whitson:** Yeah,  
  * **Devyn Grenner:** else that you need to see? Okay.  
  * **Marissa Hill-Whitson:** yeah. Basically, like, from what I could see, the main products seem to have, like, that top portion all is set up in, like, its own liquid file. So I just want to get a better understanding, like, how it's set up, how you typically make revisions to it. You, like, in terms of best practices, are we duplicating it, making the change, and then implementing it, or. I just wanted to get a better understanding of your workflow just so we can follow a similar pattern and  
  * **Devyn Grenner:** Yeah.  
  * **Marissa Hill-Whitson:** just kind of function in the same way.  
  * **Devyn Grenner:** Okay. It's a little all over the place, so I'm just gonna.  
  * **Marissa Hill-Whitson:** It's all good. I was  
  * **Alex Belanger:** With  
  * **Marissa Hill-Whitson:** poking  
  * **Alex Belanger:** web.  
  * **Marissa Hill-Whitson:** around  
  * **Alex Belanger:** It  
  * **Marissa Hill-Whitson:** and  
  * **Alex Belanger:** always  
  * **Marissa Hill-Whitson:** I  
  * **Alex Belanger:** is.  
  * **Devyn Grenner:** Okay.  
  * **Marissa Hill-Whitson:** was like,  
  * **Alex Belanger:** Don't  
  * **Marissa Hill-Whitson:** I have  
  * **Alex Belanger:** worry.  
  * **Marissa Hill-Whitson:** so many questions.  
  * **Devyn Grenner:** I'm sure you're poking around.  
  * **Marissa Hill-Whitson:** I  
  * **Devyn Grenner:** You're  
  * **Marissa Hill-Whitson:** was  
  * **Devyn Grenner:** like,  
  * **Marissa Hill-Whitson:** in  
  * **Devyn Grenner:** I.  
  * **Marissa Hill-Whitson:** staging. Don't worry. I was just like,  
  * **Devyn Grenner:** Oh, no, no. But I'm sure you were very confused. So  
  * **Marissa Hill-Whitson:** yeah, it's  
  * **Devyn Grenner:** I  
  * **Marissa Hill-Whitson:** all  
  * **Devyn Grenner:** can  
  * **Marissa Hill-Whitson:** good.  
  * **Devyn Grenner:** definitely share my screen and if you have questions, let me know. I might. I'll just, you know,  
  * **Marissa Hill-Whitson:** Yeah,  
  * **Devyn Grenner:** go  
  * **Marissa Hill-Whitson:** Bob  
  * **Devyn Grenner:** through.  
  * **Marissa Hill-Whitson:** around. It's all good.  
  * **Devyn Grenner:** Okay, one sec. Okay. Can you guys see my window? Okay, great. All right, so for. We'll just use this cement white four by four as an example. So here we have a details section, sizing illustration. We don't have to go through that. And then these kind of drawer copy sections, they all kind of come from different places. So let me really quick this. So looking at details right now, we're managing this in Accentuate within Metafields. So on the product level, we have. At the bottom of our meta fields, we have. We have product details. The way that I'm managing it right now is it's on the product level. So if we want something specific for, you know, a certain color, certain size, we can do that. If I want it to be the same across, you know, a tile category, what I'll do is I'll do an export of all of our Accentuate products using tags. So, you know, I know that white 4x4 is a part of the cement category. So I'll ex. I'll export products using a cement tag and then bulk update this within Excel  
  * **Marissa Hill-Whitson:** Okay.  
  * **Devyn Grenner:** and then import it with. Within Accentuate here.  
  * **Marissa Hill-Whitson:** Okay, that makes sense. It's good to know that you're leveraging a tool like this. Could you scroll up a bit? I just had a  
  * **Devyn Grenner:** Yeah,  
  * **Marissa Hill-Whitson:** couple of questions. So the details section, is that just so I'm understanding correctly? So that's just. If we go back to the ze front end. Not front, but like the front. Okay, so that's that section, and then the accordion section below that. Just  
  * **Devyn Grenner:** this  
  * **Marissa Hill-Whitson:** so I  
  * **Devyn Grenner:** is  
  * **Marissa Hill-Whitson:** understand.  
  * **Devyn Grenner:** coming from. Yeah, this is coming from a couple different places. Not  
  * **Marissa Hill-Whitson:** Okay.  
  * **Devyn Grenner:** where I just showed you. Yeah. So about how it's made. An installation guide is all using meta objects.  
  * **Marissa Hill-Whitson:** Yep.  
  * **Devyn Grenner:** The reason why we did this, I think, you know, we just went through a website refresh back in December, and the way that they originally built it was all in Accentuate. Right. And we found that we needed more flexibility, so we moved those three into meta objects. I think eventually it'd be nice to have them all, but it's nice to have the flexibility of having separate or unique copy on the product level. So that's kind of why we're using Accentuate for that instead of Meta objects and then just going back. So the.  
  * **Marissa Hill-Whitson:** In terms of how you're, like, able to order this, though, so do you have a custom product for the like each prop, like the category or is it more  
  * **Devyn Grenner:** So  
  * **Marissa Hill-Whitson:** so  
  * **Devyn Grenner:** how  
  * **Marissa Hill-Whitson:** on  
  * **Devyn Grenner:** we  
  * **Marissa Hill-Whitson:** a  
  * **Devyn Grenner:** order,  
  * **Marissa Hill-Whitson:** one to one?  
  * **Devyn Grenner:** order these drawers,  
  * **Marissa Hill-Whitson:** Yes.  
  * **Devyn Grenner:** they automatically are ordered. So like the. In the design, they are all the same. So we're always going to have details above size and thickness. We're always going to have about above at the top and then installation guide at the bottom. If they're not filled out, they just will drop. They just won't show.  
  * **Marissa Hill-Whitson:** I see. Okay. But  
  * **Devyn Grenner:** Yeah,  
  * **Marissa Hill-Whitson:** it's always. It's a standardized order. If we, if we were wanting to change that order, it would need to be signed.  
  * **Devyn Grenner:** like this.  
  * **Marissa Hill-Whitson:** Yeah.  
  * **Devyn Grenner:** Yeah. So we're. I connected with our developers conspire and they're working on making changes. So essentially what we want to do is bring the detail section down here and rename it and then allow for copy here that doesn't necessarily have a header. I don't have an answer for you yet on exactly where that's going to be managed or how, but I can get that information to you as soon as we have the new structure in place, essentially.  
  * **Marissa Hill-Whitson:** Okay, that makes sense. And all of this is on like none of this is available in the front end cms. Correct. It all seemed pretty custom. Okay, sounds good.  
  * **Devyn Grenner:** Yeah,  
  * **Marissa Hill-Whitson:** That makes sense to me. So basically when you're working with that team, they'll. They're mapping out a plan to potentially reorder it  
  * **Devyn Grenner:** yeah,  
  * **Marissa Hill-Whitson:** and then I guess from there it's a matter of just updating that content. So in  
  * **Devyn Grenner:** yeah.  
  * **Marissa Hill-Whitson:** terms of.  
  * **Devyn Grenner:** Just  
  * **Marissa Hill-Whitson:** I know  
  * **Devyn Grenner:** exactly.  
  * **Marissa Hill-Whitson:** you said it was pulling from a couple different places. So there's meta objects and then what was it? Accenture.  
  * **Devyn Grenner:** Accentuate.  
  * **Marissa Hill-Whitson:** Accentuate. Sorry,  
  * **Devyn Grenner:** Yeah. No, no, no, it's fine.  
  * **Marissa Hill-Whitson:** close. It was closed so they accentuate. So I guess from our perspective, if we're updating the content, just knowing where those specific content pieces live so that we're able to go in and dynamically update it would be all we need to know. But if we're not like rebuilding the template that's living with you, then totally  
  * **Devyn Grenner:** Yeah,  
  * **Marissa Hill-Whitson:** makes our life much easier  
  * **Devyn Grenner:** yeah,  
  * **Marissa Hill-Whitson:** and then we'll be able to, once we know where it lives, go in and make those dynamic changes.  
  * **Devyn Grenner:** totally. Yeah, exactly.  
  * **Marissa Hill-Whitson:** This is easy for me.  
  * **Devyn Grenner:** Yeah. Good. Okay. What'd you say?  
  * **Marissa Hill-Whitson:** I was just asking Alex if he had anything.  
  * **Devyn Grenner:** Well, there's one more place. Or do you want me to show you one more place in Accentuate where we have to make a change or do you want me to just, once we have the new structure, kind of like list things out for you again?  
  * **Marissa Hill-Whitson:** I mean let's walk through it and then we'll go through like where everything actually lives once it's like solidified, finalized and then if any changes make just like keep us posted so that we can. Yeah, we can work on it. I just want to go through your process for actually updating content and how you do it for, for these product level updates just so we're aligned as well.  
  * **Devyn Grenner:** Okay. Yeah, I think, you know, if this is a product that isn't live, it's really easy for me to just make changes and then test them out and, and see how they look before setting them live. If you're making changes to live products, which is essentially what you guys will be doing, making the changes in Accentuate or Meta objects, they'll just automatically go live. So I never, I rarely will make changes to products in staging just because we don't always update our staging with newer products. I mean, we, we certainly can, but I rarely will do that.  
  * **Marissa Hill-Whitson:** Yeah, I guess because it's built in through these like third like third party apps, for lack of a better word. You're kind of limited in terms of the staging to live environment  
  * **Devyn Grenner:** Yeah,  
  * **Marissa Hill-Whitson:** and you don't ever like duplicate draft because I guess within again what I just said that they no matter what you input, it's going to go live.  
  * **Devyn Grenner:** yeah,  
  * **Marissa Hill-Whitson:** Okay,  
  * **Devyn Grenner:** yeah,  
  * **Marissa Hill-Whitson:** so Alex, it's a really important consideration for the content team then because it's. We should probably do this in smaller batches and  
  * **Alex Belanger:** Yeah,  
  * **Marissa Hill-Whitson:** have  
  * **Alex Belanger:** I  
  * **Marissa Hill-Whitson:** it  
  * **Alex Belanger:** think that's  
  * **Marissa Hill-Whitson:** thoroughly  
  * **Alex Belanger:** a good call as  
  * **Marissa Hill-Whitson:** QA'd  
  * **Alex Belanger:** well.  
  * **Marissa Hill-Whitson:** just to limit the risk and downtime and like we want eyes on it right away.  
  * **Devyn Grenner:** yeah.  
  * **Alex Belanger:** No,  
  * **Devyn Grenner:** Maybe  
  * **Alex Belanger:** for  
  * **Devyn Grenner:** like  
  * **Alex Belanger:** sure.  
  * **Devyn Grenner:** pick one product or something and then see  
  * **Marissa Hill-Whitson:** Yeah,  
  * **Devyn Grenner:** how it looks and  
  * **Alex Belanger:** Oh  
  * **Marissa Hill-Whitson:** yeah,  
  * **Devyn Grenner:** that.  
  * **Alex Belanger:** yeah,  
  * **Devyn Grenner:** Yeah,  
  * **Alex Belanger:** no for sure. The first one that goes, we'll just do one. One at a time and then once we get that kind of process nailed in, that's when we'll kind of go in bigger batch at a time. I am curious and I apologize if My lack of development knowledge is showing, but is there a possibility to maybe start utilizing the staging site more as a precaution and kind of going through the pattern of like publishing on staging and then pushing when it's ready from staging to live. Is that something we could maybe look at just for more security or did I miss.  
  * **Marissa Hill-Whitson:** yeah. I guess  
  * **Alex Belanger:** Yeah,  
  * **Marissa Hill-Whitson:** that's  
  * **Alex Belanger:** okay,  
  * **Marissa Hill-Whitson:** what we were saying in terms of like the third party apps, when you make changes to the products, from my understanding you can correct me if I'm wrong, Devin, but when you make changes directly in that space, there is no staging environment that products are live in. The site.  
  * **Alex Belanger:** I  
  * **Marissa Hill-Whitson:** They  
  * **Alex Belanger:** see.  
  * **Marissa Hill-Whitson:** go  
  * **Alex Belanger:** Gotcha.  
  * **Marissa Hill-Whitson:** live. If  
  * **Devyn Grenner:** yeah.  
  * **Marissa Hill-Whitson:** the,  
  * **Alex Belanger:** Okay.  
  * **Marissa Hill-Whitson:** if it's like a draft product and living on the back end, then that's like more of like a playground, for lack of a better word. But yeah, we're limited  
  * **Alex Belanger:** Gotcha,  
  * **Marissa Hill-Whitson:** by like, I mean Shopify is great for that. That like you can literally make a copy of your production site, duplicate it and make it into its own theme. That's amazing. Love that. But this is  
  * **Devyn Grenner:** If  
  * **Marissa Hill-Whitson:** just a  
  * **Devyn Grenner:** everything  
  * **Marissa Hill-Whitson:** limitation.  
  * **Devyn Grenner:** is in. Yeah, if everything is,  
  * **Marissa Hill-Whitson:** Yeah,  
  * **Devyn Grenner:** you know, changed within Shopify, but unfortunately.  
  * **Marissa Hill-Whitson:** yeah, products are. It's just a global component. It's hard to mess with.  
  * **Alex Belanger:** gotcha, gotcha.  
  * **Marissa Hill-Whitson:** So  
  * **Alex Belanger:** Okay.  
  * **Marissa Hill-Whitson:** there  
  * **Alex Belanger:** No, that  
  * **Marissa Hill-Whitson:** just  
  * **Alex Belanger:** makes sense.  
  * **Marissa Hill-Whitson:** as a heads up for the team, it comes with like an inherent risk. Obviously we make small bulk. We'll make small changes versus bulk changes.  
  * **Devyn Grenner:** Okay, great.  
  * **Marissa Hill-Whitson:** I don't really know the scale of how much you're looking to update, Alex, but you and I can connect on like a good action plan for that.  
  * **Alex Belanger:** Yeah, for sure. Oh, I can say right now, so for implementation, we're looking at in total 60 to 70 content page updates a month. Within that it's going to change month by month, but on average we're looking. So for this month we're looking at 31 or actually make that 61 because we're doing March and April, both in April due to the onboarding timing.  
  * **Marissa Hill-Whitson:** Yeah.  
  * **Alex Belanger:** But yeah, there's. The first batch we got is 31 product pages,  
  * **Marissa Hill-Whitson:** Okay.  
  * **Alex Belanger:** 18 core web pages, which I don't think are going to be impacted by the kind of that third party tool that you guys mentioned since it's on product pages and then 10 new blog posts. If off top of my head, I remember correctly, the numbers.  
  * **Marissa Hill-Whitson:** Okay, cool. Yeah, we can group them by category and tackle it that way.  
  * **Alex Belanger:** Perfect. Okay. But yeah, I think for the most part that kind of concern issue was really with the products themselves, with the way that these pages are built. But.  
  * **Marissa Hill-Whitson:** Yeah, cool.  
  * **Devyn Grenner:** Okay. Yeah. And you know, some of these will be, you know, on the product level, so that'll be one change. Some will be on like the meta field, sorry, meta object level, which is like one change, but it affects a bunch of products. So I don't really know how you guys classify your Amount of pages that you are able to work on a month. But just thinking about the amount that we're looking at, you know, each category, I'm looking at cement right now. That's. It's a very large category. I think it has like over 100 products in it. So product pages. So I don't really know how we're going to tackle that. But you know, for some of the changes that you make, it's like one change for 100 products and then some are one change per product.  
  * **Marissa Hill-Whitson:** Yeah, I guess just to speak to that. So for the, like, some of these, the about section obviously is like specific to the tile itself. Am I correct in saying that? And the tile usage and then the order shipping and installation guide, are those global or specific to product category?  
  * **Devyn Grenner:** Say that one more time.  
  * **Marissa Hill-Whitson:** Sorry, can  
  * **Jamie \+ Eric Greenspan:** Oh,  
  * **Marissa Hill-Whitson:** you  
  * **Jamie \+ Eric Greenspan:** I  
  * **Marissa Hill-Whitson:** spell  
  * **Jamie \+ Eric Greenspan:** can take  
  * **Marissa Hill-Whitson:** that?  
  * **Jamie \+ Eric Greenspan:** it. It's okay, Devin. So shipping is general for all installation guides are category specific with the caveat that within a certain few categories probably. Well, the leash is an example. This is where it gets really nuanced. And we maybe need to make this in a written list for you somewhere. Like in the leash, we have one colorway called Unglazed Natural, which is our only unglazed solution that needs separate steps from all of our glazed solutions. On the ceramic side, Devin, are you familiar? We have three different finishes of our course, ceramics, and then we have some special collections and ceramics. But do those installation guides vary at all within that category? Or is really unglazed siles the only anomaly within a category level?  
  * **Devyn Grenner:** I believe that they're pretty much the same, the installation goods.  
  * **Jamie \+ Eric Greenspan:** Okay,  
  * **Devyn Grenner:** Yeah. Order.  
  * **Jamie \+ Eric Greenspan:** so  
  * **Marissa Hill-Whitson:** My  
  * **Jamie \+ Eric Greenspan:** probably  
  * **Marissa Hill-Whitson:** concern.  
  * **Jamie \+ Eric Greenspan:** just the leash and remembering that unglazed leash and any skew that includes that, including some of our most mosaics, does have a special treatment compared to our standards. Leash  
  * **Marissa Hill-Whitson:** Okay, yeah, I was basically just asking from like a quality assurance standpoint, like if we're making content changes to certain products where like all the different points that we need to double check, for instance, like the installation guide or the, the order shipping, just knowing every page that it's touching just to ensure that we're making the right edits in the right place.  
  * **Devyn Grenner:** Yeah. So, so, yeah. So within meta objects. Let's see. So for the about section, we have  
  * **Marissa Hill-Whitson:** Obviously.  
  * **Devyn Grenner:** individual meta objects and it's using the handle of, I believe, the product type.  
  * **Marissa Hill-Whitson:** Yeah, that seems very like just from at a glance, it seems very clear and descriptive. So  
  * **Devyn Grenner:** Okay,  
  * **Marissa Hill-Whitson:** yeah, it's very clear as to what we're. We need to edit. So that alleviates  
  * **Devyn Grenner:** okay,  
  * **Marissa Hill-Whitson:** my concern.  
  * **Devyn Grenner:** okay. The, you know, the tougher ones are going to be the. Probably the ones that are in accentuate. The.  
  * **Marissa Hill-Whitson:** Yeah,  
  * **Devyn Grenner:** Let's see the details and is it how it's made? Yes. So I didn't get a chance to show you this yet, but essentially details is on the product level and then how it's made is on the. The tile category level. But we are managing it through accentuate as well.  
  * **Marissa Hill-Whitson:** okay.  
  * **Devyn Grenner:** So you can see here. I'll just go to accentuate on the product type. If you want to do edit values. I went to the product or, sorry, product type. You know, you can go to each one and then update the how it's made. Why isn't this one updated? Oh, sorry. It's not how it's made. It's orders and shipping. I'm so sorry. So orders and shipping and details are in accentuate. Orders and shipping is on the product type level, Details is on the product level and the rest are in meta objects.  
  * **Marissa Hill-Whitson:** Okay. Yeah, that, that makes sense from a general perspective. But yeah, having those guidelines of what lives where will definitely be able to help our speed of implementation in that respect.  
  * **Devyn Grenner:** Yeah. And I think. I know we talked about this previously, but when we get that new structure from Conspire and I understand where everything is managed, if, if we do make any changes, I can identify that for you in email just to double down on it.  
  * **Alex Belanger:** Yeah,  
  * **Marissa Hill-Whitson:** Yeah, no,  
  * **Alex Belanger:** for  
  * **Marissa Hill-Whitson:** I  
  * **Alex Belanger:** sure.  
  * **Marissa Hill-Whitson:** appreciate that.  
  * **Devyn Grenner:** Yeah, yeah,  
  * **Alex Belanger:** Excellent. Okay. All right. So Marisa, I think we have any more questions or is that just about  
  * **Marissa Hill-Whitson:** No,  
  * **Alex Belanger:** COVID  
  * **Marissa Hill-Whitson:** I'm  
  * **Alex Belanger:** it?  
  * **Marissa Hill-Whitson:** super clear with this. That was super helpful. Thank you, Devin, for walking us through  
  * **Devyn Grenner:** yeah,  
  * **Marissa Hill-Whitson:** that. It  
  * **Devyn Grenner:** of  
  * **Marissa Hill-Whitson:** just, it's  
  * **Devyn Grenner:** course.  
  * **Marissa Hill-Whitson:** easier to see it live than trying to like piece together  
  * **Devyn Grenner:** Totally.  
  * **Marissa Hill-Whitson:** an email. So.  
  * **Devyn Grenner:** No, totally.  
  * **Marissa Hill-Whitson:** No, live demos are just easier when sometimes it comes to web  
  * **Devyn Grenner:** Yeah, yeah. Thank you for meeting today to. To show you. So,  
  * **Alex Belanger:** Oh no, of course. Yeah, I know we want to get content rolling there, so I wanted to make sure we were getting on it as soon as possible. Actually, speaking of, so what you got going on this weekend, you have tomorrow and Friday off going out of town, a little, little cottage trip maybe.  
  * **Devyn Grenner:** yes, I'm going to Palm Springs.  
  * **Alex Belanger:** Oh, amazing. That sounds so fun.  
  * **Jamie \+ Eric Greenspan:** or. Oh, I think. Sorry, guys. I didn't even realize I was still off video. Devin,  
  * **Alex Belanger:** That's  
  * **Jamie \+ Eric Greenspan:** why  
  * **Alex Belanger:** okay.  
  * **Jamie \+ Eric Greenspan:** are you going to Palm Springs?  
  * **Devyn Grenner:** I'm going to a little festival out there. I  
  * **Marissa Hill-Whitson:** weekend  
  * **Devyn Grenner:** hate the word  
  * **Marissa Hill-Whitson:** too.  
  * **Devyn Grenner:** Coachella. To go see some music. So  
  * **Alex Belanger:** Nice.  
  * **Devyn Grenner:** let me take a few days off. Yeah,  
  * **Alex Belanger:** Right on, right on.  
  * **Devyn Grenner:** yeah.  
  * **Alex Belanger:** I haven't been to a festival since Rockfest 2018 or 19\. I think it's  
  * **Devyn Grenner:** Where.  
  * **Alex Belanger:** been far  
  * **Devyn Grenner:** Where  
  * **Alex Belanger:** too  
  * **Devyn Grenner:** is  
  * **Alex Belanger:** long.  
  * **Devyn Grenner:** that? Where  
  * **Alex Belanger:** It's  
  * **Devyn Grenner:** is.  
  * **Alex Belanger:** in. So it's a Canadian festival there, but it's kind of like a Warp Tour, but like was a bit kind of more punk, bit more metal  
  * **Devyn Grenner:** I  
  * **Alex Belanger:** type  
  * **Devyn Grenner:** used to go  
  * **Alex Belanger:** stuff  
  * **Devyn Grenner:** to work  
  * **Alex Belanger:** there.  
  * **Devyn Grenner:** for all the time  
  * **Alex Belanger:** Yeah, no way.  
  * **Devyn Grenner:** back in the day.  
  * **Alex Belanger:** Yeah, I went a handful of times. Way back when I started going to Rockfest, my brother actually played Warp Tour for one show in Toronto.  
  * **Devyn Grenner:** Oh, fun.  
  * **Alex Belanger:** Yeah, I think it was. He won like a local radio battle of the bands type thing and like the first prize was playing the Ernie Ball stage. And I know that because he never stops talking to about it.  
  * **Devyn Grenner:** So cool. That's a fun fact. Like if he ever needs to just talk about something fun that he did in his past that's  
  * **Alex Belanger:** Oh  
  * **Devyn Grenner:** great.  
  * **Alex Belanger:** yeah, yeah, exactly, exactly.  
  * **Devyn Grenner:** They're all nice.  
  * **Marissa Hill-Whitson:** Icebreaker. For sure.  
  * **Devyn Grenner:** Yeah, for sure.  
  * **Jamie \+ Eric Greenspan:** Wait, Alex, tell me where you two are located. I'm trying to still get  
  * **Alex Belanger:** Oh  
  * **Jamie \+ Eric Greenspan:** a lay  
  * **Alex Belanger:** yeah,  
  * **Jamie \+ Eric Greenspan:** of the land on the link wrap side.  
  * **Marissa Hill-Whitson:** We're  
  * **Alex Belanger:** yeah,  
  * **Marissa Hill-Whitson:** both in Canada.  
  * **Jamie \+ Eric Greenspan:** You're  
  * **Alex Belanger:** yeah,  
  * **Jamie \+ Eric Greenspan:** both in Canada.  
  * **Marissa Hill-Whitson:** Yeah,  
  * **Alex Belanger:** yeah, yeah. So I'm in Ottawa and Marissa is right outside of Toronto. Right. If I  
  * **Marissa Hill-Whitson:** yeah,  
  * **Alex Belanger:** remember correctly. Yeah, yeah,  
  * **Jamie \+ Eric Greenspan:** Oh,  
  * **Alex Belanger:** yeah.  
  * **Jamie \+ Eric Greenspan:** cool. It's so funny. Our last SEO agency was Canadian too, so  
  * **Alex Belanger:** Oh, really? Oh, what's their name? I might know them. Yeah,  
  * **Jamie \+ Eric Greenspan:** they were  
  * **Alex Belanger:** yeah.  
  * **Jamie \+ Eric Greenspan:** really tiny. Monochrome was like the company name. It's this guy Cam.  
  * **Alex Belanger:** Monochrome. I'm  
  * **Jamie \+ Eric Greenspan:** They  
  * **Alex Belanger:** curious.  
  * **Jamie \+ Eric Greenspan:** came  
  * **Alex Belanger:** Huh.  
  * **Jamie \+ Eric Greenspan:** through. I'm trying to remember who referred us to them. Yeah, they were great. Just lighter touch smaller. Much, much smaller shop.  
  * **Alex Belanger:** Fair enough. A little more boutique.  
  * **Jamie \+ Eric Greenspan:** Yeah, exactly.  
  * **Alex Belanger:** Yeah. Nice.  
  * **Jamie \+ Eric Greenspan:** But go, Canada. I  
  * **Alex Belanger:** Yeah.  
  * **Marissa Hill-Whitson:** yeah,  
  * **Jamie \+ Eric Greenspan:** know you're a national anthem from my summer camp  
  * **Alex Belanger:** Really? Wait, why would you know it from summer camp? Did you like.  
  * **Jamie \+ Eric Greenspan:** because  
  * **Alex Belanger:** Would you  
  * **Jamie \+ Eric Greenspan:** it's  
  * **Alex Belanger:** come up  
  * **Jamie \+ Eric Greenspan:** in Wisconsin  
  * **Alex Belanger:** north?  
  * **Jamie \+ Eric Greenspan:** and there used to  
  * **Alex Belanger:** Oh,  
  * **Jamie \+ Eric Greenspan:** be a few  
  * **Alex Belanger:** yeah.  
  * **Jamie \+ Eric Greenspan:** people who came and so we would sing it for them. And  
  * **Alex Belanger:** Oh,  
  * **Jamie \+ Eric Greenspan:** now  
  * **Alex Belanger:** that's  
  * **Jamie \+ Eric Greenspan:** my  
  * **Alex Belanger:** nice.  
  * **Jamie \+ Eric Greenspan:** kids go to the camp and they don't sing it anymore. And I think that, like, the Canadians stopped coming and so. Oh,  
  * **Alex Belanger:** Yeah,  
  * **Jamie \+ Eric Greenspan:** Canada.  
  * **Alex Belanger:** it's the little culture war there that's been going on.  
  * **Jamie \+ Eric Greenspan:** Yep, yep. It's funny, there's, like, headlines that are like, the Canadians aren't coming to Palm Springs anymore. And they're like, yeah, we  
  * **Alex Belanger:** Oh,  
  * **Jamie \+ Eric Greenspan:** are.  
  * **Alex Belanger:** I did. Yeah. There's still lows coming. The snowbirds are going down to  
  * **Jamie \+ Eric Greenspan:** Yeah.  
  * **Alex Belanger:** Florida every year no matter what. Which, my God, it's so funny. I actually saw a CBC which is like Canada's ABC  
  * **Jamie \+ Eric Greenspan:** Okay.  
  * **Alex Belanger:** News like, documentary about snowbirds and like, they basically made like a mini Canada in Florida and like different, like retirement residents and it's so funny.  
  * **Devyn Grenner:** Oh,  
  * **Alex Belanger:** Yeah,  
  * **Marissa Hill-Whitson:** right on.  
  * **Alex Belanger:** it.  
  * **Marissa Hill-Whitson:** The golf community is here too.  
  * **Alex Belanger:** Yeah, yeah, exactly.  
  * **Devyn Grenner:** that's so funny. Oh my gosh.  
  * **Alex Belanger:** Alrighty. Oh, Jamie, actually, while you're here, do you have like a second or two to talk about the content? I just was wondering if we could get kind of your initial thoughts on that new batch we just sent over.  
  * **Jamie \+ Eric Greenspan:** Yes. So I've been focused just on Casablanca 4x4. And this is where Ryan, I don't know if you're actively on, but we're basically parallel pathing some optimizations on our end to accommodate some copy updates that we needed to make based on, like, technical directions for the tiles and specs, as well as blending that with more of your content. So where we stand now. And I can share my screen if  
  * **Alex Belanger:** Perfect.  
  * **Jamie \+ Eric Greenspan:** you guys want, like a quick preview. And this is why I've just, like, had you guys on hold for a second as we kind of get our act together over here is that I don't want to cause you more work if we're gonna  
  * **Alex Belanger:** I  
  * **Jamie \+ Eric Greenspan:** change  
  * **Alex Belanger:** don't know, Jamie,  
  * **Jamie \+ Eric Greenspan:** anything.  
  * **Alex Belanger:** we love the work over here, so please bring it on.  
  * **Jamie \+ Eric Greenspan:** Okay. So this is. Oh, wait, what am I. We're on Zoom. Let's see.  
  * **Alex Belanger:** Oh, also, Marisa, I think the rest of the call is going to be mostly content focused, so if you have a 4:30, you can feel free to jump off.  
  * **Marissa Hill-Whitson:** Okay, thank you. It was so nice seeing you guys again and I look forward to seeing the updated content set up. And then if I have any questions, I'll let you know. Thank  
  * **Devyn Grenner:** Amazing.  
  * **Marissa Hill-Whitson:** you.  
  * **Jamie \+ Eric Greenspan:** Thank you.  
  * **Devyn Grenner:** Nice to  
  * **Marissa Hill-Whitson:** Bye.  
  * **Devyn Grenner:** meet you.  
  * **Marissa Hill-Whitson:** Have a good rest of your day.  
  * **Jamie \+ Eric Greenspan:** Okay. All right, so here was our challenge, is that right now I'm just mimicking this because I think I'm only sharing one window, but our collection pages are really only showing the HERO  
  * **Alex Belanger:** Mm,  
  * **Jamie \+ Eric Greenspan:** with nothing under that, coupled with more copy, coupled with the copy that has been currently at the top of the pdps, which. This is a category page, so that's a little bit of a different journey. We'll start here, though. The main initiative here was to show a peak below the hero.  
  * **Alex Belanger:** mm. Yeah,  
  * **Jamie \+ Eric Greenspan:** Considering  
  * **Alex Belanger:** just kind of  
  * **Jamie \+ Eric Greenspan:** where  
  * **Alex Belanger:** bumping  
  * **Jamie \+ Eric Greenspan:** the bullet  
  * **Alex Belanger:** a bit of content a little further up, right?  
  * **Jamie \+ Eric Greenspan:** just. Yeah, I was concerned that people would not know that there was product on the page and bounce, and we really wanted to ensure that people knew that. So we're mocking up a couple directions, but namely kind of getting this menu here and. Or this copy here above the fold.  
  * **Alex Belanger:** Mm, mm.  
  * **Jamie \+ Eric Greenspan:** So that's what's happening on the collection page on the pdp. Hold on. I'm not used to sharing on Zoom.  
  * **Alex Belanger:** Yeah, no worries.  
  * **Jamie \+ Eric Greenspan:** Devin, do you want to. I'm trying to find our, like, PDP mock up.  
  * **Devyn Grenner:** It's the emails. Quick. PDP  
  * **Jamie \+ Eric Greenspan:** Oh, here.  
  * **Devyn Grenner:** updates  
  * **Jamie \+ Eric Greenspan:** Yeah, there we are. Okay. So this is. What is the most relevant on the PDP for this exercise is.  
  * **Devyn Grenner:** or I can. Yeah.  
  * **Jamie \+ Eric Greenspan:** So right now we were leading with. I don't know if I can share my whole window, but what was happening is we were leading with details. Do you see my cursor?  
  * **Alex Belanger:** Yeah, yeah, I do.  
  * **Jamie \+ Eric Greenspan:** Okay, we were leading with these details up here. That just said details and that was the only copy that was visible above the accordion. The  
  * **Alex Belanger:** Mm,  
  * **Jamie \+ Eric Greenspan:** problem was as we were adding in more of the technical details that were driven by our side, it was skewing very negative to the point that I was worried that would impact conversions negatively.  
  * **Alex Belanger:** mm,  
  * **Jamie \+ Eric Greenspan:** So what I've done here is I pulled some of the copy from the about. You can see that your keyword terms still are highlighted here, which  
  * **Alex Belanger:** mm.  
  * **Jamie \+ Eric Greenspan:** was crucial to keep.  
  * **Alex Belanger:** No,  
  * **Jamie \+ Eric Greenspan:** So  
  * **Alex Belanger:** absolutely.  
  * **Jamie \+ Eric Greenspan:** I. I wanted to basically pull up the more positive brand and tile category and language here, put in high level notes here that were like the warning, and then still have this outside of the accordion. But this copy is a little bit more of the Zia LED update. That's technical but also a little bit scary for people. Like, we're basically calling out, this could take two to three times longer to install  
  * **Alex Belanger:** Yeah.  
  * **Jamie \+ Eric Greenspan:** than an  
  * **Alex Belanger:** It's  
  * **Jamie \+ Eric Greenspan:** average  
  * **Alex Belanger:** kind of like,  
  * **Jamie \+ Eric Greenspan:** tile.  
  * **Alex Belanger:** for lack of better term, like the legal jargon, you kind of have to  
  * **Jamie \+ Eric Greenspan:** Yeah,  
  * **Alex Belanger:** say,  
  * **Jamie \+ Eric Greenspan:** but  
  * **Alex Belanger:** yeah,  
  * **Jamie \+ Eric Greenspan:** like, also don't buy this tile. It's going to cost you three times to install. Right. So I couldn't lead with that.  
  * **Alex Belanger:** no,  
  * **Jamie \+ Eric Greenspan:** I  
  * **Alex Belanger:** for  
  * **Jamie \+ Eric Greenspan:** still  
  * **Alex Belanger:** sure  
  * **Jamie \+ Eric Greenspan:** need  
  * **Alex Belanger:** you  
  * **Jamie \+ Eric Greenspan:** people  
  * **Alex Belanger:** want  
  * **Jamie \+ Eric Greenspan:** to  
  * **Alex Belanger:** it.  
  * **Jamie \+ Eric Greenspan:** buy  
  * **Alex Belanger:** Yeah.  
  * **Jamie \+ Eric Greenspan:** it. So in doing this, we're switching our structure up a bit, which is why I wanted you guys not to go forward with more than 30 right now, because essentially, it's the same kind of copy, but we just want to shift a little where it goes,  
  * **Alex Belanger:** Oh yeah. And  
  * **Jamie \+ Eric Greenspan:** so.  
  * **Alex Belanger:** honestly, like from like our perspective, our side, in terms of like the actual content writing delivery, this switch up doesn't really impact anything. It's just where  
  * **Jamie \+ Eric Greenspan:** Okay.  
  * **Alex Belanger:** we put that information in that like Google Docs, where, like, it does kind of pop up is when we go to add it to the page itself on the live.  
  * **Jamie \+ Eric Greenspan:** Okay.  
  * **Alex Belanger:** But as long as we get the sign off on the actual, like, content copy for like right now, that's kind of like the priority there. And then it's just a matter of reshuffling the order of, like, the information. Granted, because we want to do a bit more of a snapshot about the about section. There might be a few that we need to redraft a new section, but we're looking at a paragraph, so really wouldn't take that long to pull that out of what we currently have for the more detailed about section.  
  * **Jamie \+ Eric Greenspan:** Okay, great. So, yeah, we'll still have this. This hasn't changed on our end. The accordion at the bottom. It's more. I don't know now if we'll have some redundancy where we might need to revisit this about if we're pulling some of it up here. But I figured this might actually help you guys. Having this language on top and not in an accordion. Is that better for search?  
  * **Alex Belanger:** Definitely it pulls it out basically the way that like, copy impacts, like SEO. It's all about the kind of relevant information like at the top and just kind of  
  * **Jamie \+ Eric Greenspan:** Great.  
  * **Alex Belanger:** slowly going down. So the order of the information definitely plays a role. And of course, you know, making sure it's got the proper like headline or not headlines, but like headers, footers, H1 tags, all that good stuff there. But really having that kind of top information as like the kind of main snippet like early on the page. Definitely priority or not priority. But best practice.  
  * **Devyn Grenner:** Jamie, are we doing this for. Eventually doing this for all products or is it just for certain categories?  
  * **Jamie \+ Eric Greenspan:** This would be for all  
  * **Devyn Grenner:** Okay.  
  * **Jamie \+ Eric Greenspan:** just because right now, like, let me do a quick spot check. Sorry, I  
  * **Alex Belanger:** It's  
  * **Jamie \+ Eric Greenspan:** have been  
  * **Alex Belanger:** okay.  
  * **Jamie \+ Eric Greenspan:** very scattered. I just want to make sure. Let me look at, like, toroso. Yeah. Right now, like, we're leading with the details, and there's no brand copy there. So in this holistic revisit that we're doing what I wanted to do both from a conversion and brand perspective, but also my gut was saying that this will help you guys and, like, all of our initiatives more is to move some of that copy up so that there is a little more context on a product page other than just the technical details of the product.  
  * **Alex Belanger:** Yeah,  
  * **Jamie \+ Eric Greenspan:** Like, we had some of that fluff, but the way we redesigned our site, it got buried. And now that SEO is the focus, I wanted to bring that back out and also soften the blow if there are less sexy or scary notes in the details. I don't want to lead with, like, that granular, icky stuff. Right. Like, that can still be above the accordion when it's this important. But I think this feels better from both a brand and marketing perspective, but also a conversion perspective and an SEO perspective.  
  * **Alex Belanger:** yeah,  
  * **Jamie \+ Eric Greenspan:** So  
  * **Alex Belanger:** no,  
  * **Jamie \+ Eric Greenspan:** I  
  * **Alex Belanger:** I.  
  * **Jamie \+ Eric Greenspan:** kind of wanted to catch it all before we go through this whole exercise, since it's been snowballing since we had that updated text, and that text sort of worsened the detail section as far as, like, palatability for a shopper. So that's where I just wanted to pause real quick. Devin's like, I'm going to kill you and just attack this before we go through the rest of this full PDP refresh exercise.  
  * **Alex Belanger:** Yeah, no, no worries at all. So in terms of next steps then what we can do if this is for sure, like the finalized. I kind of break down of how you the page, which if I'm not mistaken seems to be the exact same as slide four in that slide deck that you sent over. I can send this to the content team to update the 31 pages to match the kind of flow of it and pull out and then we can kind of hold off on actual publishing once we have the updated product page and the web side done.  
  * **Jamie \+ Eric Greenspan:** Okay,  
  * **Alex Belanger:** Good news. By the end of this week, possibly tomorrow, we'll see how the editing is going. Today we're just doing final edits to the core page updates  
  * **Jamie \+ Eric Greenspan:** Great.  
  * **Alex Belanger:** so the collection pages as well as the blog posts. So we will have some content we can work with and start publishing right away  
  * **Jamie \+ Eric Greenspan:** Amazing.  
  * **Alex Belanger:** and like approval. So all good there and then just the 31 product pages might be a little bit slower just  
  * **Jamie \+ Eric Greenspan:** Yeah.  
  * **Alex Belanger:** because of the web stuff there. But  
  * **Jamie \+ Eric Greenspan:** Yeah.  
  * **Alex Belanger:** yeah, no problems and  
  * **Jamie \+ Eric Greenspan:** And  
  * **Alex Belanger:** yeah,  
  * **Jamie \+ Eric Greenspan:** as soon as we get. Devin's been working with our web agency on some of the, like,  
  * **Devyn Grenner:** Structural.  
  * **Jamie \+ Eric Greenspan:** structural updates  
  * **Devyn Grenner:** Yeah.  
  * **Jamie \+ Eric Greenspan:** and Redesign on the pdp. So as soon as that is ready to preview in like a state outside of my photo inbox, which I  
  * **Alex Belanger:** Yeah,  
  * **Jamie \+ Eric Greenspan:** think I did that in slides because I'm so savvy, will send you what that's going to look like and then confirm like the back end setup of that as well. So thank you  
  * **Alex Belanger:** gotcha.  
  * **Jamie \+ Eric Greenspan:** for your brief pause there. Hopefully that'll move really quickly  
  * **Alex Belanger:** Yeah,  
  * **Jamie \+ Eric Greenspan:** and  
  * **Alex Belanger:** no worries.  
  * **Jamie \+ Eric Greenspan:** I think it'll help us all going forward, both from a revenue perspective, but also from the SEO discovery.  
  * **Alex Belanger:** No, absolutely. And then what we'll do since we had the last half of April, focusing on like the April deliverables just because that, you know, the timing of the onboarding and everything, we're kind of doing  
  * **Jamie \+ Eric Greenspan:** Yeah,  
  * **Alex Belanger:** two months in one. I'll make sure that we prioritize the other category and blog pages as like the content and then save  
  * **Jamie \+ Eric Greenspan:** great.  
  * **Alex Belanger:** the product pages as last to help give a bit more time  
  * **Jamie \+ Eric Greenspan:** Great.  
  * **Alex Belanger:** as well.  
  * **Jamie \+ Eric Greenspan:** Yeah. Blogs we can fly with  
  * **Alex Belanger:** Excellent. Excellent.  
  * **Jamie \+ Eric Greenspan:** and those you are able to train with Devin on how to update. And you guys will do the updates or you'll be handing them over in docs and Devin will have to build them. Remind me how that flow works.  
  * **Alex Belanger:** Oh,  
  * **Jamie \+ Eric Greenspan:** Have we talked  
  * **Alex Belanger:** it's  
  * **Jamie \+ Eric Greenspan:** about it?  
  * **Alex Belanger:** kind of. I guess we haven't really talked about it  
  * **Jamie \+ Eric Greenspan:** Yeah.  
  * **Alex Belanger:** that much. So typically like we can do either way. Some clients we work for, they prefer uploading themselves. Personally, I like doing as much of the work ourselves just to kind of help, you know, you hire us for a reason to kind of, you know, take over the weight of the site. Right. So if you have a preference on you rather kind of Devin take on publishing, we can do that. But we are more than happy to do the publishing ourselves. And what we would typically do, especially the first round of it, we'll send you. What we typically do is we'll do like a draft mode on staging, send you a link to that to kind of review, get a final look and feel of it. And then once you hit approve, we just go ahead and kind of push it live from there.  
  * **Jamie \+ Eric Greenspan:** Cool.  
  * **Devyn Grenner:** Are these.  
  * **Jamie \+ Eric Greenspan:** Yeah, maybe we even slow it down a bit and have Devin take the lead on like the first couple. Just to walk you through the different templates and layouts and like, kind of how she would approach it and. And then we can like flip that and you guys do a few. Put it on staging.  
  * **Alex Belanger:** Sure.  
  * **Jamie \+ Eric Greenspan:** We get in a good groove with that, maybe work. Because, Devin, I know we have like.  
  * **Devyn Grenner:** Yeah, I guess my question, you know, maybe I missed this, is are these new blog posts or edits to existing ones?  
  * **Alex Belanger:** Oh, yeah. So for the blog post, it's brand new content, so  
  * **Devyn Grenner:** Okay.  
  * **Alex Belanger:** new pages. And what we would typically do is we build it off like the existing templates to match like the kind of look and feel. And then we're also doing updates to the collection pages and adding more content and copy there. So do we have a double prong content approach? We're doing some  
  * **Devyn Grenner:** Yeah.  
  * **Alex Belanger:** optimizing some new content. Yeah,  
  * **Devyn Grenner:** Okay, cool. Yeah, I'm happy to help whenever needed, I guess. Jamie, just scheduling. I'm curious because I'll be out  
  * **Jamie \+ Eric Greenspan:** Yeah, yeah.  
  * **Devyn Grenner:** the remainder of the week and Monday. So what are you thinking for timeline, I guess for  
  * **Jamie \+ Eric Greenspan:** Well,  
  * **Devyn Grenner:** my.  
  * **Jamie \+ Eric Greenspan:** you're. Do you have those blogs ready? Like, should we schedule for next week when Devin's back or do you guys need to.  
  * **Alex Belanger:** they should be coming ready by tomorrow and then that's when I'm going to have like my look through it and then I might get the team to make a few changes. So by Friday morning, we should have it all ready your way. And  
  * **Jamie \+ Eric Greenspan:** Yeah,  
  * **Alex Belanger:** then if you  
  * **Jamie \+ Eric Greenspan:** so  
  * **Alex Belanger:** have any  
  * **Jamie \+ Eric Greenspan:** when  
  * **Alex Belanger:** feedback  
  * **Jamie \+ Eric Greenspan:** you're back,  
  * **Alex Belanger:** for  
  * **Jamie \+ Eric Greenspan:** Devin,  
  * **Alex Belanger:** us,  
  * **Jamie \+ Eric Greenspan:** it's,  
  * **Devyn Grenner:** Okay.  
  * **Jamie \+ Eric Greenspan:** it's. It doesn't need to happen overnight, so.  
  * **Devyn Grenner:** Okay. And then  
  * **Jamie \+ Eric Greenspan:** Yeah,  
  * **Devyn Grenner:** the product. The product pages, is that after that or is that more urgent?  
  * **Alex Belanger:** from my understanding, we'll do the product pages after we get like the updated products with the other web team that you mentioned, the outsource organizer.  
  * **Devyn Grenner:** Right, right. But Jamie, I'm not gonna be here, so I just wanted. I just want to understand, are we going to update those as soon as Conspire has the new, like, live structure? Are we able to make those changes while I'm gone or do you think it'll be probably next week? Week.  
  * **Jamie \+ Eric Greenspan:** well, I'm gonna be on a shoot off Friday too, so. Nothing needs to happen this week until you're back, Devin.  
  * **Devyn Grenner:** Okay. Okay, cool.  
  * **Jamie \+ Eric Greenspan:** Yeah, yeah, don't worry about that.  
  * **Devyn Grenner:** Okay.  
  * **Jamie \+ Eric Greenspan:** I mean, it's all urgent, but it's not urgent enough to do it when Devin and I are both unreachable. So, like,  
  * **Devyn Grenner:** Yeah,  
  * **Jamie \+ Eric Greenspan:** no  
  * **Devyn Grenner:** yeah,  
  * **Jamie \+ Eric Greenspan:** one needs to panic. Next week's a lot more open for me. I don't know about you, Devin, but  
  * **Devyn Grenner:** yeah.  
  * **Jamie \+ Eric Greenspan:** yeah,  
  * **Devyn Grenner:** I.  
  * **Jamie \+ Eric Greenspan:** I think we'll work on like, you guys catching up the next couple days and then I'll be more reachable on Friday. I can't necessarily hop on meetings, but I'll be monitoring email from a shoe and Devin will hurrah, be fully out of pocket the rest of the week. So that we'll just dive into this next week, but  
  * **Devyn Grenner:** Perfect. Okay.  
  * **Jamie \+ Eric Greenspan:** it should  
  * **Devyn Grenner:** That  
  * **Jamie \+ Eric Greenspan:** move  
  * **Devyn Grenner:** totally.  
  * **Jamie \+ Eric Greenspan:** pretty quickly. And the blog stuff, I mean, I don't want to say it's like super creative, but like, you know, there are creative decisions Devin makes and layout and  
  * **Alex Belanger:** Oh, for sure. Yeah,  
  * **Jamie \+ Eric Greenspan:** there's  
  * **Alex Belanger:** we want to  
  * **Jamie \+ Eric Greenspan:** options.  
  * **Alex Belanger:** make sure that.  
  * **Jamie \+ Eric Greenspan:** So I just want her to be able to walk you guys through that. And I don't Think we'll be overly precious. That's the name of this game is we're trying to really relax and, you know, let. Let things just happen because it's not going to be realistic. But I'll probably, like, be able to do. I'm a really fast editor, so, like, I'll probably, at least at the beginning, you know, still take a pass at the blog copy before it goes in. But again, that'll be like same day turn. I'm not going to go through levels of approvals. Just like, here's a quick pass, let's go.  
  * **Alex Belanger:** Yeah,  
  * **Jamie \+ Eric Greenspan:** And then eventually I'm hoping that will stop and then we'll just be able to crank. So  
  * **Alex Belanger:** yeah, absolutely. Well, I think after the initial product pages, we definitely got a much better grasp of the voice and tone and stuff, which is going to translate very nicely into the blogs and the  
  * **Jamie \+ Eric Greenspan:** great.  
  * **Alex Belanger:** collection pages. So should be solid. But I definitely, I still want you to kind of give that, especially on the first few. Just give it the final review, make sure you're happy with it there and then. Yeah, off to the races.  
  * **Jamie \+ Eric Greenspan:** Amazing. And again, I, you know, I'm reminding everyone on our team that there is a learning curve with tile and there's a lot of nuances with these materials and installation and how we talk about glazes, not glazed. So please don't feel like we're judging you for not being up to speed day one, because Devin and I learn on the daily new things about these materials and how we are to speak about them and speak about their installation. So just know that, like, unfortunately this is a category where there's a lot of nuance and a lot of really granular details that are very important, but that no one is faulting you for not being up to speed with us or with our product team because it's like, it's a lot. It's a lot  
  * **Alex Belanger:** Yeah,  
  * **Jamie \+ Eric Greenspan:** and very specific. So  
  * **Alex Belanger:** no, for sure. Yeah, I appreciate that. And yeah, we're aiming to kind of catch up on that. Not slowly but surely, but fast and surely.  
  * **Jamie \+ Eric Greenspan:** great.  
  * **Alex Belanger:** Excellent.  
  * **Jamie \+ Eric Greenspan:** Well, thank you so much.  
  * **Alex Belanger:** Yeah, absolutely. And just to reconfirm, I just want to make sure. Just one last thing. So do we want to assume that this is the kind of final format? Because I can get my content team to start working on reshuffling the product page just now or do we want to hold off? If you want to make a few tweaks to it some more over the next few days.  
  * **Devyn Grenner:** Yeah. I mean, Jamie, I think. I think this is the. This would be the final as far as content, like input for you guys. I definitely think this is final where you have the content up top, you have the order and installation content below, and then you have the about through installation guides below. We might explore moving the about and installation tabs even further below into a different module, but they're going to be directly below, I think just. It's more of a visual change rather than removing them altogether. So as far as I think you guys are concerned for copy input, this is. This is going to be final.  
  * **Alex Belanger:** Okay, perfect. I will give that feedback back to the team for the 31 product pages, get those updated and should be good to go.  
  * **Jamie \+ Eric Greenspan:** Oh, I forgot I sent you that. Sorry, guys.  
  * **Alex Belanger:** Oh, no, you're  
  * **Jamie \+ Eric Greenspan:** Great,  
  * **Alex Belanger:** okay.  
  * **Jamie \+ Eric Greenspan:** great, great. I'm. Yeah,  
  * **Alex Belanger:** Long day, huh? Yeah,  
  * **Devyn Grenner:** You're  
  * **Alex Belanger:** no,  
  * **Devyn Grenner:** great.  
  * **Alex Belanger:** I  
  * **Jamie \+ Eric Greenspan:** I'm great, great, great.  
  * **Alex Belanger:** feel you, Jamie. For some reason, I Woke up at 4am this morning and could not for the life of me fall back asleep.  
  * **Jamie \+ Eric Greenspan:** Ah,  
  * **Alex Belanger:** So it's been. It's been. It's been one of those  
  * **Jamie \+ Eric Greenspan:** that's  
  * **Alex Belanger:** days.  
  * **Devyn Grenner:** Wait,  
  * **Jamie \+ Eric Greenspan:** tough.  
  * **Devyn Grenner:** I Woke up at 4,5.45 and I was complaining about that, so at  
  * **Alex Belanger:** Oh,  
  * **Devyn Grenner:** least it wasn't.  
  * **Alex Belanger:** what?  
  * **Jamie \+ Eric Greenspan:** 5:30  
  * **Devyn Grenner:** I'm so sorry.  
  * **Jamie \+ Eric Greenspan:** is  
  * **Alex Belanger:** Love  
  * **Jamie \+ Eric Greenspan:** my  
  * **Alex Belanger:** it.  
  * **Jamie \+ Eric Greenspan:** normal. Wake  
  * **Alex Belanger:** Oh,  
  * **Jamie \+ Eric Greenspan:** up, guys.  
  * **Alex Belanger:** normal.  
  * **Devyn Grenner:** No,  
  * **Alex Belanger:** Wake up.  
  * **Devyn Grenner:** Jamie,  
  * **Alex Belanger:** Actually,  
  * **Jamie \+ Eric Greenspan:** Yeah,  
  * **Alex Belanger:** I was surprised when you, when you responded back to me like early on I was like, wait, isn't it like 6am or something right there? Like 6 or 7 there. But.  
  * **Jamie \+ Eric Greenspan:** well,  
  * **Devyn Grenner:** classic.  
  * **Jamie \+ Eric Greenspan:** the worst is when I work, like later on weekends. I always intend to, like, schedule my emails for like, business hours. And then sometimes I forget and I like, emailed something on Easter and I'm like, like, guys, this was not supposed to come through today. Like, delete this email.  
  * **Alex Belanger:** Yeah, I'm bad. I'm bad for that as well. Yeah, it's always like two minutes later it's like, ah, I could have scheduled that. Oops.  
  * **Devyn Grenner:** It's. It's  
  * **Alex Belanger:** Right  
  * **Devyn Grenner:** just  
  * **Alex Belanger:** on.  
  * **Devyn Grenner:** so easy to press bend, you know?  
  * **Alex Belanger:** Yeah, exactly.  
  * **Devyn Grenner:** Is that.  
  * **Alex Belanger:** Just one and done and just on  
  * **Devyn Grenner:** Yeah.  
  * **Alex Belanger:** to the next piece.  
  * **Devyn Grenner:** Yeah. All  
  * **Alex Belanger:** All  
  * **Devyn Grenner:** right,  
  * **Alex Belanger:** righty. Well,  
  * **Jamie \+ Eric Greenspan:** Well,  
  * **Alex Belanger:** yeah, I  
  * **Jamie \+ Eric Greenspan:** thank  
  * **Alex Belanger:** guess.  
  * **Jamie \+ Eric Greenspan:** you all for connecting these dots when my brain is not at full capacity, but excited, excited to keep moving. Thank you so much. And I know this is like a slight pivot, but I think it will  
  * **Alex Belanger:** Oh  
  * **Jamie \+ Eric Greenspan:** be  
  * **Alex Belanger:** that's okay.  
  * **Jamie \+ Eric Greenspan:** best going forward. So  
  * **Alex Belanger:** No, absolutely  
  * **Jamie \+ Eric Greenspan:** just keep us posted as these pieces come in. I'll do a path on the blog post and then we can schedule a time for you guys and Devin, I don't think I need to be on that to do a walkthrough of some of the setup. And then as far as the PDP stuff, I'll look through that a little more once we reformat it to this structure, and then we'll go from there.  
  * **Alex Belanger:** perfect. Sounds like a plan. Yeah, Devin,  
  * **Jamie \+ Eric Greenspan:** Thank  
  * **Alex Belanger:** I'll  
  * **Jamie \+ Eric Greenspan:** you.  
  * **Alex Belanger:** email over a few meeting times for next week, like Tuesday or Wednesday probably.  
  * **Devyn Grenner:** perfect.  
  * **Alex Belanger:** And then when you get back on Tuesday, just like let me know which ones work best and we'll get that going.  
  * **Devyn Grenner:** Awesome. Sounds good. Thank you.  
  * **Alex Belanger:** All right,  
  * **Jamie \+ Eric Greenspan:** Thank  
  * **Alex Belanger:** thank you  
  * **Jamie \+ Eric Greenspan:** you,  
  * **Alex Belanger:** both.  
  * **Jamie \+ Eric Greenspan:** guys.  
  * **Alex Belanger:** Take care. And Devin, enjoy. I want to hear all about.  
  * **Devyn Grenner:** Thanks. I might still be recovering on Tuesday, so I'll  
  * **Alex Belanger:** Fair  
  * **Devyn Grenner:** let you  
  * **Alex Belanger:** enough,  
  * **Devyn Grenner:** know.  
  * **Alex Belanger:** fair enough.  
  * **Jamie \+ Eric Greenspan:** Maybe Wednesday.  
  * **Devyn Grenner:** Yeah, exactly. All right, have  
  * **Alex Belanger:** All  
  * **Devyn Grenner:** a  
  * **Alex Belanger:** right,  
  * **Jamie \+ Eric Greenspan:** All  
  * **Devyn Grenner:** good  
  * **Alex Belanger:** take  
  * **Devyn Grenner:** weekend.  
  * **Jamie \+ Eric Greenspan:** right,  
  * **Alex Belanger:** care  
  * **Jamie \+ Eric Greenspan:** we'll  
  * **Alex Belanger:** everyone.  
  * **Jamie \+ Eric Greenspan:** talk soon. Thank you all.  
  * **Devyn Grenner:** Bye.  
  * **Jamie \+ Eric Greenspan:** Bye.
