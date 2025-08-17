"""
Negotiator Skill - Smart Price Negotiation and Deal Finding
Helps users find better deals and negotiate prices responsibly
"""

import logging
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json

logger = logging.getLogger(__name__)

class Negotiator:
    """
    Negotiator system for finding deals and providing negotiation assistance
    Focuses on ethical negotiation strategies and price comparison
    """
    
    def __init__(self, digital_twin):
        self.twin = digital_twin
        self.negotiation_history = []
        
        # Common negotiation contexts
        self.negotiation_contexts = {
            'retail': ['store', 'shop', 'buy', 'purchase', 'price'],
            'service': ['service', 'contractor', 'repair', 'maintenance'],
            'subscription': ['subscription', 'plan', 'membership', 'monthly'],
            'salary': ['salary', 'raise', 'promotion', 'compensation'],
            'rent': ['rent', 'lease', 'apartment', 'housing'],
            'car': ['car', 'vehicle', 'auto', 'dealership']
        }
        
    def route(self, text: str, require_confirm: bool = True) -> str:
        """Route negotiation requests"""
        try:
            text_lower = text.lower()
            
            # Price comparison requests
            if any(phrase in text_lower for phrase in ['compare prices', 'find deals', 'best price']):
                return self._handle_price_comparison(text)
            
            # Negotiation strategy requests
            elif any(phrase in text_lower for phrase in ['negotiate', 'lower price', 'discount', 'deal']):
                return self._provide_negotiation_strategies(text)
            
            # Subscription optimization
            elif any(phrase in text_lower for phrase in ['subscription', 'monthly payment', 'cancel subscription']):
                return self._handle_subscription_optimization(text)
            
            # Service negotiation
            elif any(phrase in text_lower for phrase in ['service quote', 'contractor', 'estimate']):
                return self._handle_service_negotiation(text)
            
            # Salary negotiation
            elif any(phrase in text_lower for phrase in ['salary negotiation', 'raise', 'promotion']):
                return self._handle_salary_negotiation()
            
            # General negotiation advice
            else:
                return self._provide_general_negotiation_advice(text)
                
        except Exception as e:
            logger.error(f"Error in negotiator routing: {e}")
            return f"Negotiation assistance error: {e}"
    
    def _handle_price_comparison(self, text: str) -> str:
        """Handle price comparison requests"""
        return """💰 **Smart Price Comparison Guide**

**Best Price Comparison Strategies:**

🔍 **Online Tools:**
- Google Shopping - Compare prices across retailers
- PriceGrabber - Track price history
- Shopping browser extensions (Honey, Capital One Shopping)
- Amazon price tracking tools (CamelCamelCamel)

📱 **Mobile Apps:**
- Flipp - Grocery store flyers and deals
- Rakuten - Cashback and coupons
- Target, Walmart apps - Store-specific deals
- Gas station apps - Fuel price comparison

🛒 **Shopping Strategies:**
1. **Check multiple retailers** - Don't settle for first price
2. **Look for coupon codes** - Search "[store name] coupon"
3. **Check clearance sections** - Hidden deals
4. **Consider refurbished items** - Often like-new condition
5. **Time your purchases** - End of season sales

💡 **Pro Tips:**
- Clear browser cookies before shopping (avoid price tracking)
- Use incognito mode for unbiased prices
- Check social media for flash sales
- Sign up for price drop alerts
- Consider total cost (shipping, taxes, warranties)

**Price Comparison Checklist:**
□ Base price at 3+ retailers
□ Shipping costs included
□ Return policy reviewed
□ Warranty/protection plans
□ Customer reviews checked
□ Alternative brands considered

**Red Flags:**
❌ Prices significantly below market (scams)
❌ No return policy
❌ Poor customer reviews
❌ Unfamiliar websites
❌ Pressure to "buy now"

What specific item are you looking to compare prices for?"""
    
    def _provide_negotiation_strategies(self, text: str) -> str:
        """Provide context-specific negotiation strategies"""
        # Detect negotiation context
        context = self._detect_negotiation_context(text)
        
        base_strategies = """🤝 **Effective Negotiation Strategies**

**Universal Principles:**
1. **Do Your Research** - Know market prices and alternatives
2. **Be Polite but Firm** - Respect while advocating for yourself
3. **Listen Actively** - Understand the other party's position
4. **Be Prepared to Walk Away** - Your strongest negotiation tool
5. **Look for Win-Win Solutions** - Benefits for both parties

**Preparation Checklist:**
□ Research market rates/prices
□ Know your budget and limits
□ Identify your alternatives (BATNA)
□ Understand timing factors
□ Practice your key points

**During Negotiation:**
✅ Start with a reasonable but ambitious offer
✅ Justify your position with facts
✅ Ask questions to understand their constraints
✅ Look for creative solutions
✅ Be patient - don't rush decisions

**Common Mistakes to Avoid:**
❌ Making the first offer too low/high
❌ Getting emotional or personal
❌ Revealing your maximum budget early
❌ Accepting the first counteroffer
❌ Negotiating when desperate"""
        
        if context == 'retail':
            return base_strategies + """

**🛍️ Retail-Specific Tips:**
- Ask about price matching policies
- Inquire about upcoming sales
- Consider bundling items for discounts
- Ask for manager if salesperson can't help
- Time purchases during clearance seasons
- Check if you qualify for student/military discounts"""
        
        elif context == 'service':
            return base_strategies + """

**🔧 Service Negotiation Tips:**
- Get multiple quotes (3+ recommended)
- Ask about off-season discounts
- Inquire about bundling services
- Negotiate payment terms, not just price
- Ask about warranties and guarantees
- Consider partial DIY to reduce costs"""
        
        elif context == 'subscription':
            return base_strategies + """

**📺 Subscription Negotiation:**
- Call retention department (say "cancel")
- Mention competitor offers
- Ask about promotional rates
- Request billing date changes
- Inquire about feature downgrades
- Consider annual vs. monthly payments"""
        
        else:
            return base_strategies + "\n\nFor specific negotiation contexts, please let me know what you're negotiating (retail, service, subscription, etc.)."
    
    def _handle_subscription_optimization(self, text: str) -> str:
        """Handle subscription optimization requests"""
        return """📺 **Subscription Optimization Strategy**

**Audit Your Subscriptions:**
🔍 **Discovery Methods:**
- Check bank/credit card statements
- Review app store subscriptions
- Look at email receipts
- Use subscription tracking apps (Truebill, Mint)

📊 **Common Subscriptions to Review:**
- Streaming services (Netflix, Hulu, Disney+)
- Music services (Spotify, Apple Music)
- Software subscriptions (Adobe, Office)
- News and magazine subscriptions
- Fitness and wellness apps
- Cloud storage services

**Optimization Strategies:**

💰 **Immediate Savings:**
1. **Cancel unused subscriptions** - Free up money instantly
2. **Downgrade plans** - Reduce features you don't use
3. **Annual billing** - Often 15-20% cheaper than monthly
4. **Family plans** - Share costs with family/friends
5. **Student discounts** - If eligible, significant savings

📞 **Negotiation Tactics:**
- Call to cancel (retention offers)
- Mention competitor pricing
- Ask about promotional rates
- Request loyalty discounts
- Negotiate temporary pauses instead of cancellation

🔄 **Rotation Strategy:**
- Subscribe only when actively using
- Rotate streaming services seasonally
- Use free trials strategically
- Cancel and resubscribe for new user offers

**Subscription Management Tools:**
✅ **Tracking Apps:**
- Truebill (now Rocket Money)
- Mint
- Personal Capital
- Bank subscription alerts

✅ **Calendar Reminders:**
- Set reminders before renewal dates
- Track free trial end dates
- Note annual subscription renewals

**Red Flags - Consider Canceling:**
❌ Haven't used in 30+ days
❌ Can get similar service free/cheaper
❌ Subscribed during trial and forgot
❌ Lifestyle change made it irrelevant
❌ Financial priorities have shifted

**Before You Cancel:**
1. Check if you can pause instead
2. See if you can downgrade
3. Ask family if they use it
4. Consider seasonal reactivation
5. Export any important data

Want help creating a personalized subscription audit plan?"""
    
    def _handle_service_negotiation(self, text: str) -> str:
        """Handle service-based negotiation requests"""
        return """🔧 **Service Negotiation Masterclass**

**Getting Multiple Quotes:**
📋 **Quote Checklist:**
- Get 3-5 written estimates
- Ensure quotes include same scope of work
- Ask about material vs. labor costs
- Clarify timeline and milestones
- Verify license and insurance
- Check references and reviews

**Timing Your Negotiations:**
⏰ **Best Times to Negotiate:**
- Off-season (e.g., HVAC in spring/fall)
- End of month/quarter (salespeople need numbers)
- Slow business periods
- When you're not desperate
- During economic downturns

**Service-Specific Strategies:**

🏠 **Home Services (Plumbing, Electric, HVAC):**
- Bundle multiple projects
- Ask about first-time customer discounts
- Negotiate payment schedules
- Inquire about warranty extensions
- Consider providing your own materials

🚗 **Auto Services:**
- Bring your own parts (if allowed)
- Ask about service package deals
- Negotiate on labor rates
- Request loaner car provisions
- Ask about loyalty programs

🏡 **Home Improvement:**
- Get detailed material breakdowns
- Negotiate on change order rates
- Ask about bulk discounts
- Consider seasonal timing
- Request cleanup inclusion

**Negotiation Conversation Starters:**
💬 "I've received quotes ranging from $X to $Y. What can you do to earn my business?"
💬 "I'm ready to start immediately. Is there any flexibility on the price?"
💬 "I have several projects. Can we discuss a package deal?"
💬 "What would it cost to add [additional service] to this quote?"

**Payment Negotiation:**
💳 **Options to Discuss:**
- Cash discount (2-5% typical)
- Extended payment terms
- Progress payments vs. full upfront
- Material cost transparency
- Warranty and guarantee terms

**Red Flags - Walk Away:**
❌ Significant upfront payment required
❌ Door-to-door solicitation
❌ Pressure to sign immediately
❌ No written contract
❌ Prices significantly below others
❌ No license/insurance verification

**Documentation Tips:**
📝 **Get Everything in Writing:**
- Detailed scope of work
- Materials specifications
- Labor hours and rates
- Timeline and milestones
- Warranty terms
- Change order procedures

**After Agreement:**
✅ Schedule regular check-ins
✅ Document any changes
✅ Pay according to agreed schedule
✅ Maintain professional relationship
✅ Leave honest reviews

Need help with a specific type of service negotiation?"""
    
    def _handle_salary_negotiation(self) -> str:
        """Handle salary negotiation requests"""
        return """💼 **Professional Salary Negotiation Guide**

**⚠️ Important:** Salary negotiation is highly personal and context-dependent. This is general guidance only.

**Research Phase:**
📊 **Salary Research Tools:**
- Glassdoor, PayScale, Salary.com
- LinkedIn Salary Insights
- Robert Half Salary Guide
- Industry-specific reports
- Local job postings

🎯 **Key Factors to Research:**
- Market rate for your role/location
- Company's salary ranges
- Your performance metrics
- Company financial health
- Industry standards and trends

**Preparation Checklist:**
□ Document your achievements
□ Quantify your contributions (metrics, $, %)
□ Research market compensation
□ Know your minimum acceptable offer
□ Prepare alternative compensation options
□ Plan timing for the conversation

**Negotiation Strategies:**

💪 **Building Your Case:**
1. **Performance Evidence** - Specific achievements
2. **Market Data** - External salary research
3. **Value Add** - How you've contributed to company success
4. **Future Potential** - Your growth trajectory
5. **Additional Responsibilities** - Expanded role scope

🗣️ **Conversation Approach:**
- Schedule dedicated meeting time
- Present facts, not emotions
- Listen to employer's perspective
- Be open to creative solutions
- Maintain professional demeanor

**Beyond Base Salary:**
💰 **Total Compensation Package:**
- Bonus structure and targets
- Stock options or equity
- Vacation time and flexibility
- Professional development budget
- Health benefits and wellness perks
- Retirement contribution matching
- Work-from-home options

**Timing Considerations:**
⏰ **Best Times to Negotiate:**
- Annual review periods
- After successful project completion
- When taking on new responsibilities
- During job offer process
- When you have competing offers

❌ **Avoid These Times:**
- During company financial stress
- Right after poor performance
- In group settings
- Via email (do in person/video)
- When you're emotional

**Handling Responses:**

✅ **If They Say Yes:**
- Get agreement in writing
- Confirm start date for new compensation
- Express gratitude professionally
- Continue strong performance

❌ **If They Say No:**
- Ask about timeline for reconsideration
- Inquire about performance milestones
- Discuss non-monetary benefits
- Request feedback on improvement areas
- Consider your options professionally

**Sample Conversation Starters:**
💬 "Based on my research and performance, I'd like to discuss my compensation..."
💬 "I've taken on additional responsibilities and would like to review my salary..."
💬 "Given my achievements this year, I believe a salary adjustment is warranted..."

**Professional Development:**
📈 **Ongoing Strategies:**
- Keep achievement records updated
- Continuously develop skills
- Build internal relationships
- Understand company goals
- Seek feedback regularly

**Remember:** Negotiation is a professional conversation, not a confrontation. Focus on value, facts, and mutual benefit.

Would you like help preparing for a specific aspect of salary negotiation?"""
    
    def _detect_negotiation_context(self, text: str) -> str:
        """Detect the context of negotiation from text"""
        text_lower = text.lower()
        
        for context, keywords in self.negotiation_contexts.items():
            if any(keyword in text_lower for keyword in keywords):
                return context
        
        return 'general'
    
    def _provide_general_negotiation_advice(self, text: str) -> str:
        """Provide general negotiation advice"""
        return """🤝 **General Negotiation Wisdom**

**Core Principles:**
1. **Preparation is Key** - Knowledge is power in negotiation
2. **Win-Win Mindset** - Look for solutions that benefit both parties
3. **Patience Pays Off** - Good deals take time
4. **Know Your BATNA** - Best Alternative to Negotiated Agreement
5. **Emotional Intelligence** - Manage emotions, read the room

**The Negotiation Process:**

🎯 **Phase 1: Preparation**
- Research market rates/standards
- Identify your goals and limits
- Understand the other party's needs
- Prepare supporting documentation
- Plan your opening position

🗣️ **Phase 2: Opening**
- Build rapport first
- Ask questions to understand their position
- Present your case with facts
- Listen more than you speak
- Stay professional and respectful

⚖️ **Phase 3: Bargaining**
- Make reasonable counteroffers
- Look for creative alternatives
- Focus on interests, not positions
- Use "if-then" conditional proposals
- Be willing to compromise

✅ **Phase 4: Closing**
- Summarize key agreements
- Get commitments in writing
- Clarify next steps and timelines
- Express appreciation
- Follow up as needed

**Psychological Tactics (Ethical):**

🧠 **Building Influence:**
- Use reciprocity (offer something first)
- Create urgency (real deadlines only)
- Show social proof (others' choices)
- Appeal to consistency (their stated values)
- Build genuine rapport

**Communication Tips:**
💬 **Effective Language:**
- "Help me understand..." (seek clarification)
- "What if we..." (explore alternatives)
- "That's interesting..." (acknowledge without agreeing)
- "I appreciate that..." (show respect)
- "Let's explore..." (collaborative approach)

**Body Language:**
- Maintain eye contact
- Use open postures
- Mirror their communication style
- Stay calm and confident
- Take notes (shows seriousness)

**Common Negotiation Mistakes:**
❌ Starting with your best offer
❌ Getting personal or emotional
❌ Talking too much, listening too little
❌ Focusing only on price
❌ Being inflexible on creative solutions
❌ Accepting first offer too quickly

**Advanced Strategies:**
🎨 **Creative Problem Solving:**
- Package deals and bundles
- Timing and payment flexibility
- Non-monetary value adds
- Shared risk arrangements
- Future consideration promises

**When to Walk Away:**
🚪 **Exit Criteria:**
- Terms don't meet your minimum requirements
- Other party is dishonest or unethical
- Emotional atmosphere becomes toxic
- Better alternatives are available
- Gut feeling says "no"

**After the Negotiation:**
✅ **Follow-up Actions:**
- Document all agreements
- Confirm understanding via email
- Set up progress check-ins
- Maintain the relationship
- Learn from the experience

**Remember:** Good negotiation creates value for everyone involved. It's not about "winning" but finding solutions that work.

What specific negotiation situation would you like help with?"""
    
    def track_negotiation_outcome(self, negotiation_type: str, outcome: str, savings: float = 0):
        """Track negotiation outcomes for learning"""
        try:
            outcome_data = {
                'type': negotiation_type,
                'outcome': outcome,
                'savings': savings,
                'timestamp': datetime.now().isoformat()
            }
            
            self.negotiation_history.append(outcome_data)
            
            # Store in digital twin if available
            if self.twin:
                self.twin.db.record_metric('negotiation_success', 1.0 if outcome == 'success' else 0.0, outcome_data)
            
            logger.info(f"Tracked negotiation outcome: {negotiation_type} - {outcome}")
            
        except Exception as e:
            logger.error(f"Error tracking negotiation outcome: {e}")
    
    def get_negotiation_tips_for_personality(self, personality_traits: Dict[str, float]) -> List[str]:
        """Get personalized negotiation tips based on personality"""
        tips = []
        
        # Confidence-based tips
        confidence = personality_traits.get('confidence', 0.5)
        if confidence < 0.4:
            tips.append("Practice your negotiation points beforehand to build confidence")
            tips.append("Start with smaller, lower-stakes negotiations to build skills")
        elif confidence > 0.8:
            tips.append("Be careful not to come across as overconfident or aggressive")
            tips.append("Listen actively to build trust and rapport")
        
        # Technical orientation
        technical = personality_traits.get('technical_orientation', 0.5)
        if technical > 0.7:
            tips.append("Use data and facts to support your negotiation position")
            tips.append("Prepare detailed analysis and comparisons")
        else:
            tips.append("Focus on relationship building and mutual benefits")
            tips.append("Use stories and examples to illustrate your points")
        
        # General tips
        tips.extend([
            "Remember that negotiation is a conversation, not a confrontation",
            "Always be prepared to walk away if terms don't meet your needs",
            "Look for creative solutions that benefit both parties"
        ])
        
        return tips
